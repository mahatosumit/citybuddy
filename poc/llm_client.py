"""Thin async wrapper around emergentintegrations for the CityBrain POC.

Provides three primitives used across the orchestration layer:
  - llm_text:   plain text generation
  - llm_json:   structured JSON generation (router + merger)
  - llm_vision: multimodal (image + prompt) generation for the Vision agent
"""
import os
import json
import re
import base64
import logging
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# POC runs outside the backend process, so load the backend env explicitly.
load_dotenv("/app/backend/.env")

from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent

logger = logging.getLogger("citybrain.llm")

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")

# Model tiers (Google Gemini via Emergent universal key)
REASONING_MODEL = "gemini-3.1-pro-preview"   # deep multi-agent synthesis
FAST_MODEL = "gemini-2.5-flash"              # routing + quick tasks
VISION_MODEL = "gemini-2.5-flash"            # multimodal image understanding


def _new_chat(system_message: str, session_id: str, model: str) -> LlmChat:
    if not EMERGENT_LLM_KEY:
        raise RuntimeError("EMERGENT_LLM_KEY is not set in environment")
    return LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=session_id,
        system_message=system_message,
    ).with_model("gemini", model)


def _extract_json(raw: str) -> Dict[str, Any]:
    """Best-effort parse of a JSON object from model output."""
    if raw is None:
        raise ValueError("Empty LLM response")
    text = raw.strip()
    # Strip markdown fences if present
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: grab the first balanced-looking object
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start:end + 1])
        raise


async def llm_text(system: str, prompt: str, model: str = FAST_MODEL,
                   session_id: str = "poc-text") -> str:
    chat = _new_chat(system, session_id, model)
    return await chat.send_message(UserMessage(text=prompt))


async def llm_json(system: str, prompt: str, model: str = FAST_MODEL,
                   session_id: str = "poc-json") -> Dict[str, Any]:
    chat = _new_chat(system, session_id, model).with_params(
        response_format={"type": "json_object"}
    )
    raw = await chat.send_message(UserMessage(text=prompt))
    return _extract_json(raw)


async def llm_vision(system: str, prompt: str, image_base64: str,
                     model: str = VISION_MODEL,
                     session_id: str = "poc-vision") -> str:
    chat = _new_chat(system, session_id, model)
    msg = UserMessage(text=prompt, file_contents=[ImageContent(image_base64=image_base64)])
    return await chat.send_message(msg)


def bytes_to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")
