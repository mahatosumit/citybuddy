"""Async wrapper around emergentintegrations for CityBrain.

Primitives:
  - llm_text:   plain text
  - llm_json:   structured JSON (router + merger)
  - llm_vision: multimodal image understanding (Vision agent)
  - stream_text: token stream for the chat UI

Models (Google Gemini via Emergent universal key) are locked after the
Phase 1 POC validated them.
"""
import os
import re
import json
import base64
import logging
from pathlib import Path
from typing import Any, Dict, AsyncGenerator, Optional, List

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

from emergentintegrations.llm.chat import (
    LlmChat, UserMessage, ImageContent, TextDelta, StreamDone,
)

logger = logging.getLogger("citybrain.llm")

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")

REASONING_MODEL = "gemini-3.1-pro-preview"
FAST_MODEL = "gemini-2.5-flash"
VISION_MODEL = "gemini-2.5-flash"


def _new_chat(system_message: str, session_id: str, model: str,
              history: Optional[List[Dict[str, Any]]] = None) -> LlmChat:
    if not EMERGENT_LLM_KEY:
        raise RuntimeError("EMERGENT_LLM_KEY not configured")
    initial = [{"role": "system", "content": system_message}]
    if history:
        initial.extend(history)
    return LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=session_id,
        system_message=system_message,
        initial_messages=initial,
    ).with_model("gemini", model)


def extract_json(raw: str) -> Dict[str, Any]:
    if not raw:
        raise ValueError("Empty LLM response")
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start:end + 1])
        raise


async def llm_text(system: str, prompt: str, model: str = FAST_MODEL,
                   session_id: str = "cb-text") -> str:
    chat = _new_chat(system, session_id, model)
    return await chat.send_message(UserMessage(text=prompt))


async def llm_json(system: str, prompt: str, model: str = FAST_MODEL,
                   session_id: str = "cb-json") -> Dict[str, Any]:
    chat = _new_chat(system, session_id, model).with_params(
        response_format={"type": "json_object"}
    )
    raw = await chat.send_message(UserMessage(text=prompt))
    return extract_json(raw)


async def llm_vision(system: str, prompt: str, image_base64: str,
                     model: str = VISION_MODEL, session_id: str = "cb-vision") -> str:
    chat = _new_chat(system, session_id, model)
    msg = UserMessage(text=prompt, file_contents=[ImageContent(image_base64=image_base64)])
    return await chat.send_message(msg)


async def stream_text(system: str, prompt: str, model: str = FAST_MODEL,
                      session_id: str = "cb-stream",
                      history: Optional[List[Dict[str, Any]]] = None
                      ) -> AsyncGenerator[str, None]:
    chat = _new_chat(system, session_id, model, history=history)
    async for ev in chat.stream_message(UserMessage(text=prompt)):
        if isinstance(ev, TextDelta):
            yield ev.content
        elif isinstance(ev, StreamDone):
            break


def bytes_to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")
