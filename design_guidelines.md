{
  "brand": {
    "product_name": "CityBuddy — Your AI Companion for Nepal",
    "design_personality": {
      "attributes": [
        "premium (Apple-level polish)",
        "calmly adventurous (Himalayan, not cliché)",
        "trustworthy + safety-forward (Emergency Mode)",
        "fast + responsive (Linear-like)",
        "warm hospitality (Airbnb-like)"
      ],
      "visual_metaphors": [
        "Himalayan strata: layered surfaces + subtle elevation",
        "heritage craft: micro-patterns as 2–4% opacity noise/texture (never loud)",
        "wayfinding: chips, pins, route lines, and ‘decision cards’ that feel navigational"
      ],
      "do_not": [
        "No purple for AI/chat branding",
        "No cliché Nepal flag motifs or heavy mandala patterns",
        "No transparent backgrounds with dark fonts",
        "No gradient-heavy UI (see gradient restriction rule)"
      ]
    }
  },

  "typography": {
    "google_fonts": {
      "heading": {
        "family": "Space Grotesk",
        "weights": ["500", "600", "700"],
        "usage": "H1/H2, section titles, key numbers (weather, budget totals)"
      },
      "body": {
        "family": "Figtree",
        "weights": ["400", "500", "600"],
        "usage": "Body, UI labels, chat content"
      },
      "mono": {
        "family": "IBM Plex Mono",
        "weights": ["400", "500"],
        "usage": "Route steps, coordinates, debug/agent traces, code-like snippets"
      }
    },
    "tailwind_type_scale": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight",
      "h2": "text-base md:text-lg font-medium text-muted-foreground",
      "h3": "text-xl sm:text-2xl font-semibold",
      "body": "text-sm sm:text-base leading-relaxed",
      "small": "text-xs sm:text-sm text-muted-foreground",
      "chip": "text-xs font-medium"
    },
    "copy_tone": {
      "principles": [
        "Decision-first: lead with the recommendation, then the reasoning",
        "Local clarity: include Nepali terms when helpful, with short English gloss",
        "Safety language: calm, direct, non-alarmist"
      ],
      "examples": {
        "recommendation": "Go to Patan Durbar Square now — it’s quieter before sunset and the light is perfect for photos.",
        "reasoning": "Based on your pace, current traffic, and the rain window starting at 6:10 PM.",
        "emergency": "If you feel shaking: Drop, Cover, Hold On. Move away from glass."
      }
    }
  },

  "color_system": {
    "notes": [
      "Distinctly Nepal-inspired but modern: indigo night-sky + warm saffron + stone/slate neutrals + sand warmth.",
      "All colors must pass WCAG AA; for outdoor/map contexts, prefer higher contrast than AA.",
      "Avoid saturated gradients; use solids for reading surfaces."
    ],
    "palette": {
      "primary_indigo": "#1E2A5A",
      "primary_indigo_dark": "#AFC2FF",
      "accent_saffron": "#F59E0B",
      "accent_saffron_soft": "#FDBA74",
      "teal_route": "#0EA5A4",
      "success": "#16A34A",
      "warning": "#F59E0B",
      "danger": "#DC2626",
      "bg_snow": "#FBFBFA",
      "bg_night": "#0B1220",
      "surface_white": "#FFFFFF",
      "surface_dark": "#0F1A2E",
      "stone": "#E7E5E4",
      "slate_text": "#0F172A",
      "muted_text": "#475569"
    },
    "semantic_tokens_hsl": {
      "light": {
        "--background": "30 20% 99%",
        "--foreground": "222 47% 11%",
        "--card": "0 0% 100%",
        "--card-foreground": "222 47% 11%",
        "--popover": "0 0% 100%",
        "--popover-foreground": "222 47% 11%",
        "--primary": "226 50% 24%",
        "--primary-foreground": "0 0% 100%",
        "--secondary": "24 20% 96%",
        "--secondary-foreground": "226 50% 24%",
        "--muted": "24 18% 95%",
        "--muted-foreground": "215 16% 35%",
        "--accent": "38 92% 50%",
        "--accent-foreground": "222 47% 11%",
        "--destructive": "0 84% 55%",
        "--destructive-foreground": "0 0% 100%",
        "--border": "24 12% 88%",
        "--input": "24 12% 88%",
        "--ring": "226 50% 24%",
        "--radius": "0.9rem",
        "--chart-1": "226 50% 24%",
        "--chart-2": "173 70% 35%",
        "--chart-3": "38 92% 50%",
        "--chart-4": "215 16% 35%",
        "--chart-5": "0 84% 55%"
      },
      "dark": {
        "--background": "222 55% 8%",
        "--foreground": "210 40% 98%",
        "--card": "222 55% 10%",
        "--card-foreground": "210 40% 98%",
        "--popover": "222 55% 10%",
        "--popover-foreground": "210 40% 98%",
        "--primary": "226 90% 85%",
        "--primary-foreground": "222 47% 11%",
        "--secondary": "222 35% 16%",
        "--secondary-foreground": "210 40% 98%",
        "--muted": "222 35% 16%",
        "--muted-foreground": "215 20% 70%",
        "--accent": "38 92% 55%",
        "--accent-foreground": "222 47% 11%",
        "--destructive": "0 70% 45%",
        "--destructive-foreground": "210 40% 98%",
        "--border": "222 30% 18%",
        "--input": "222 30% 18%",
        "--ring": "38 92% 55%",
        "--radius": "0.9rem",
        "--chart-1": "226 90% 85%",
        "--chart-2": "173 70% 40%",
        "--chart-3": "38 92% 55%",
        "--chart-4": "215 20% 70%",
        "--chart-5": "0 70% 45%"
      }
    },
    "gradients": {
      "allowed_usage": [
        "Hero section background only (max 20% viewport)",
        "Large decorative overlays behind map header", 
        "Never on text-heavy cards"
      ],
      "recipes": {
        "hero_skyline": "radial-gradient(1200px circle at 20% 10%, rgba(245,158,11,0.18), transparent 55%), radial-gradient(900px circle at 80% 0%, rgba(14,165,164,0.14), transparent 50%), linear-gradient(180deg, rgba(30,42,90,0.06), transparent 40%)",
        "dark_aurora": "radial-gradient(900px circle at 15% 0%, rgba(14,165,164,0.18), transparent 55%), radial-gradient(900px circle at 85% 10%, rgba(245,158,11,0.14), transparent 55%)"
      }
    }
  },

  "design_tokens_css": {
    "instructions": "Main agent should replace the default shadcn tokens in /app/frontend/src/index.css with these values (keep Tailwind layers). Also set body font-family to Figtree and headings via utility classes.",
    "css_snippet": "@layer base {\n  :root {\n    --background: 30 20% 99%;\n    --foreground: 222 47% 11%;\n    --card: 0 0% 100%;\n    --card-foreground: 222 47% 11%;\n    --popover: 0 0% 100%;\n    --popover-foreground: 222 47% 11%;\n    --primary: 226 50% 24%;\n    --primary-foreground: 0 0% 100%;\n    --secondary: 24 20% 96%;\n    --secondary-foreground: 226 50% 24%;\n    --muted: 24 18% 95%;\n    --muted-foreground: 215 16% 35%;\n    --accent: 38 92% 50%;\n    --accent-foreground: 222 47% 11%;\n    --destructive: 0 84% 55%;\n    --destructive-foreground: 0 0% 100%;\n    --border: 24 12% 88%;\n    --input: 24 12% 88%;\n    --ring: 226 50% 24%;\n    --radius: 0.9rem;\n\n    /* extra app tokens */\n    --surface-2: 24 18% 97%;\n    --shadow-color: 222 47% 11%;\n    --focus-ring: 226 50% 24%;\n    --route: 173 70% 35%;\n    --saffron: 38 92% 50%;\n  }\n\n  .dark {\n    --background: 222 55% 8%;\n    --foreground: 210 40% 98%;\n    --card: 222 55% 10%;\n    --card-foreground: 210 40% 98%;\n    --popover: 222 55% 10%;\n    --popover-foreground: 210 40% 98%;\n    --primary: 226 90% 85%;\n    --primary-foreground: 222 47% 11%;\n    --secondary: 222 35% 16%;\n    --secondary-foreground: 210 40% 98%;\n    --muted: 222 35% 16%;\n    --muted-foreground: 215 20% 70%;\n    --accent: 38 92% 55%;\n    --accent-foreground: 222 47% 11%;\n    --destructive: 0 70% 45%;\n    --destructive-foreground: 210 40% 98%;\n    --border: 222 30% 18%;\n    --input: 222 30% 18%;\n    --ring: 38 92% 55%;\n\n    --surface-2: 222 35% 14%;\n    --shadow-color: 222 47% 2%;\n    --focus-ring: 38 92% 55%;\n    --route: 173 70% 40%;\n    --saffron: 38 92% 55%;\n  }\n}\n\n@layer base {\n  body {\n    font-family: \"Figtree\", ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, \"Apple Color Emoji\", \"Segoe UI Emoji\";\n  }\n}\n"
  },

  "layout_and_grid": {
    "app_shell": {
      "desktop": {
        "pattern": "Left sidebar + top utility row + content area. Map pages can use full-height split view.",
        "sidebar_width": "w-[280px] xl:w-[304px]",
        "content_max_width": "max-w-[1200px] for reading pages; map pages are full-bleed",
        "gutter": "px-4 sm:px-6 lg:px-8",
        "sticky": ["top utility bar", "chat composer", "map search row"]
      },
      "mobile": {
        "pattern": "Bottom tab bar (5 items max) + optional floating action button for ‘Ask CityBrain’.",
        "safe_area": "pb-[calc(env(safe-area-inset-bottom)+72px)]",
        "tap_targets": "min-h-[44px] (planning), min-h-[56px] (driving/emergency quick actions)"
      }
    },
    "page_templates": {
      "landing": "Hero (short) + quick actions + featured cities + trust/safety strip + testimonials + footer",
      "chat": "Two-column on desktop: chat thread + right rail ‘Decision Cards’. Single column on mobile with collapsible rail.",
      "explore": "Map + list split view on desktop; map full-screen with bottom sheet cards on mobile.",
      "detail": "Sticky header with actions + photo carousel + facts grid + reviews + nearby",
      "planner": "Timeline itinerary + map preview + regenerate controls",
      "emergency": "High-contrast, minimal choices, one-primary-action-per-section"
    }
  },

  "components": {
    "component_path": {
      "shadcn_primary": "/app/frontend/src/components/ui",
      "use_components": [
        "button.jsx",
        "card.jsx",
        "badge.jsx",
        "tabs.jsx",
        "sheet.jsx",
        "drawer.jsx",
        "dialog.jsx",
        "command.jsx",
        "scroll-area.jsx",
        "separator.jsx",
        "skeleton.jsx",
        "tooltip.jsx",
        "toggle-group.jsx",
        "switch.jsx",
        "calendar.jsx",
        "carousel.jsx",
        "progress.jsx",
        "sonner.jsx"
      ]
    },
    "global_navigation": {
      "desktop_sidebar": {
        "structure": [
          "Brand row (CityBuddy + status dot)",
          "Primary nav (Chat, Explore, Planner, Weather, Budget)",
          "Secondary (Camera AI, Nepal Intelligence, Emergency)",
          "Footer (Theme toggle, Language toggle, Profile)"
        ],
        "interaction": "Active item uses left accent bar + subtle background; hover reveals tooltip labels when collapsed.",
        "tailwind": "bg-card/80 backdrop-blur supports-[backdrop-filter]:bg-card/60 border-r",
        "data_testids": {
          "sidebar": "app-sidebar",
          "nav-chat": "nav-chat",
          "nav-explore": "nav-explore",
          "nav-planner": "nav-planner",
          "nav-emergency": "nav-emergency",
          "theme-toggle": "theme-toggle",
          "language-toggle": "language-toggle"
        }
      },
      "mobile_bottom_tabs": {
        "items": ["Chat", "Explore", "Planner", "Saved", "Profile"],
        "pattern": "Use a frosted bar (solid in dark mode) with 1px border; icons from lucide-react.",
        "tailwind": "fixed bottom-0 inset-x-0 z-50 border-t bg-background/92 backdrop-blur supports-[backdrop-filter]:bg-background/70",
        "data_testids": {
          "bottom-tabs": "bottom-tabs",
          "tab-chat": "tab-chat",
          "tab-explore": "tab-explore",
          "tab-planner": "tab-planner",
          "tab-saved": "tab-saved",
          "tab-profile": "tab-profile"
        }
      }
    },

    "citybrain_chat": {
      "thread": {
        "pattern": "Streaming chat with message groups + ‘agent chips’ + decision cards.",
        "message_bubbles": {
          "user": "bg-primary text-primary-foreground rounded-2xl rounded-br-md",
          "assistant": "bg-card border rounded-2xl rounded-bl-md",
          "assistant_emphasis": "Use a left border accent (route teal) for ‘Decision’ messages: border-l-4 border-l-[hsl(var(--route))]",
          "spacing": "max-w-[78ch] leading-relaxed"
        },
        "agent_chips": {
          "component": "badge.jsx + toggle-group.jsx",
          "style": "Small pill chips with icon + label (Travel, Food, Hotel, Weather...). Active chip uses accent background.",
          "tailwind": "rounded-full px-2.5 py-1 text-xs bg-muted hover:bg-muted/70",
          "data_testids": {
            "agent-chip": "agent-chip",
            "reasoning-toggle": "reasoning-toggle"
          }
        },
        "composer": {
          "component": "textarea.jsx + button.jsx + tooltip.jsx",
          "pattern": "Sticky bottom composer with attachments (camera), mic (future), and send.",
          "tailwind": "sticky bottom-0 bg-background/95 backdrop-blur border-t p-3",
          "micro_interactions": [
            "Send button press scale: active:scale-[0.98]",
            "Textarea auto-grow; show character hint only when near limit",
            "Streaming indicator: 3-dot pulse (CSS)"
          ],
          "data_testids": {
            "chat-input": "chat-input",
            "chat-send": "chat-send",
            "chat-attach-camera": "chat-attach-camera",
            "chat-stop-stream": "chat-stop-stream"
          }
        }
      },
      "decision_cards": {
        "pattern": "Perplexity-like structured cards: ‘Top pick’, ‘Alternatives’, ‘Why’, ‘Cost’, ‘Time’, ‘Safety’, ‘Book later’.",
        "component": "card.jsx + accordion.jsx + badge.jsx + button.jsx",
        "layout": "Desktop right rail (w-[360px]) with ScrollArea; mobile as Drawer/Sheet.",
        "tailwind": "shadow-[0_10px_30px_-18px_hsl(var(--shadow-color)/0.35)]",
        "data_testids": {
          "decision-card": "decision-card",
          "decision-card-save": "decision-card-save",
          "decision-card-open-map": "decision-card-open-map"
        }
      },
      "explainability": {
        "pattern": "Collapsed ‘Why this’ section with bullet reasoning + sources + confidence meter.",
        "component": "accordion.jsx + progress.jsx",
        "confidence": "Use Progress with route teal; label: Low/Med/High",
        "data_testids": {
          "why-this-accordion": "why-this-accordion",
          "confidence-meter": "confidence-meter"
        }
      }
    },

    "explore_map_list": {
      "desktop_split": {
        "pattern": "Resizable panels: left list, right map (or vice versa).",
        "component": "resizable.jsx + scroll-area.jsx",
        "sizes": "List min 360px, map min 420px",
        "data_testids": {
          "explore-split": "explore-split",
          "explore-list": "explore-list",
          "explore-map": "explore-map"
        }
      },
      "mobile_bottom_sheet": {
        "pattern": "Map full-screen; results as Drawer bottom sheet with snap points (25/60/92%).",
        "component": "drawer.jsx",
        "data_testids": {
          "explore-results-drawer": "explore-results-drawer",
          "explore-filter-button": "explore-filter-button"
        }
      },
      "filter_chips": {
        "component": "toggle-group.jsx + badge.jsx",
        "pattern": "Horizontal scroll chips: Hotels, Food, Attractions, Events, Safety, ‘Open now’, ‘Near me’.",
        "tailwind": "flex gap-2 overflow-x-auto no-scrollbar py-2",
        "data_testids": {
          "filter-chip": "filter-chip",
          "filter-open-now": "filter-open-now",
          "filter-near-me": "filter-near-me"
        }
      },
      "place_card": {
        "component": "card.jsx + aspect-ratio.jsx + badge.jsx + button.jsx",
        "pattern": "Photo left (or top on mobile), name + rating + distance + quick actions (Save, Directions).",
        "tailwind": "group rounded-2xl border bg-card hover:bg-muted/30 transition-colors",
        "micro_interactions": [
          "Hover: image subtle zoom via transform on img only (not container)",
          "Save: heart fills with saffron accent",
          "Card focus: ring-2 ring-[hsl(var(--focus-ring))]"
        ],
        "data_testids": {
          "place-card": "place-card",
          "place-card-save": "place-card-save",
          "place-card-directions": "place-card-directions"
        }
      },
      "map_pins": {
        "style": "Category icons (lucide) inside squircle pin; confirmed itinerary pins larger than suggestions.",
        "colors": {
          "hotel": "indigo",
          "food": "saffron",
          "attraction": "teal",
          "emergency": "red"
        }
      }
    },

    "place_detail": {
      "hero": {
        "component": "carousel.jsx + aspect-ratio.jsx",
        "pattern": "Photo carousel with subtle gradient scrim for title overlay (scrim only).",
        "data_testids": {
          "place-hero-carousel": "place-hero-carousel"
        }
      },
      "facts_grid": {
        "component": "card.jsx + separator.jsx",
        "pattern": "2x3 grid: hours, price, best time, accessibility, safety notes, local etiquette.",
        "tailwind": "grid grid-cols-2 lg:grid-cols-3 gap-3"
      },
      "reviews": {
        "component": "tabs.jsx + scroll-area.jsx",
        "pattern": "Tabs: Overview, Reviews, Tips, Nearby",
        "data_testids": {
          "place-tabs": "place-tabs"
        }
      }
    },

    "trip_planner": {
      "timeline": {
        "pattern": "Day-by-day timeline with draggable stops (phase later). For now: reorder buttons.",
        "component": "card.jsx + accordion.jsx + button.jsx",
        "tailwind": "space-y-3",
        "data_testids": {
          "itinerary-day": "itinerary-day",
          "itinerary-regenerate": "itinerary-regenerate",
          "itinerary-save": "itinerary-save"
        }
      },
      "map_preview": {
        "pattern": "Small map preview card with route line teal and day toggle.",
        "component": "card.jsx + tabs.jsx"
      }
    },

    "weather": {
      "widgets": {
        "pattern": "Glanceable cards: Now, Next 6 hours, 7-day. Use icons + precipitation probability.",
        "component": "card.jsx + badge.jsx",
        "tailwind": "grid gap-3 sm:grid-cols-2 lg:grid-cols-3",
        "data_testids": {
          "weather-now": "weather-now",
          "weather-forecast": "weather-forecast"
        }
      }
    },

    "budget": {
      "breakdown": {
        "pattern": "Horizontal bar chart for categories + list for entries.",
        "library": "recharts",
        "component": "card.jsx + table.jsx",
        "data_testids": {
          "budget-summary": "budget-summary",
          "budget-add-expense": "budget-add-expense"
        }
      }
    },

    "emergency_mode": {
      "principles": [
        "High contrast, no gradients, minimal choices",
        "One-primary-action-per-section",
        "Large tap targets (min 56px)"
      ],
      "layout": {
        "pattern": "Top: ‘Call now’ row (Police/Ambulance/Fire). Middle: nearest facilities. Bottom: guidance cards.",
        "component": "card.jsx + button.jsx + alert.jsx",
        "tailwind": "bg-destructive/5 dark:bg-destructive/10"
      },
      "data_testids": {
        "emergency-call-police": "emergency-call-police",
        "emergency-call-ambulance": "emergency-call-ambulance",
        "emergency-call-fire": "emergency-call-fire",
        "emergency-nearest-hospital": "emergency-nearest-hospital",
        "emergency-guidance": "emergency-guidance"
      }
    }
  },

  "motion_and_microinteractions": {
    "library": {
      "primary": "framer-motion",
      "usage": [
        "Page transitions (fade + slight y)",
        "Chat streaming indicators",
        "Map/list card entrance",
        "Bottom sheet snap transitions"
      ]
    },
    "principles": [
      "Motion communicates state change (not decoration)",
      "Keep durations short: 120–220ms for UI, 260–420ms for panels",
      "Respect prefers-reduced-motion"
    ],
    "recipes": {
      "card_hover": "hover:shadow-[0_18px_50px_-30px_hsl(var(--shadow-color)/0.55)] hover:-translate-y-0.5 transition-[box-shadow,background-color]",
      "button": "transition-[background-color,box-shadow,color,border-color] active:scale-[0.98]",
      "list_item_enter": "initial={{opacity:0,y:8}} animate={{opacity:1,y:0}} transition={{duration:0.18}}"
    }
  },

  "accessibility": {
    "requirements": [
      "WCAG AA contrast for all text",
      "Visible focus rings (ring-2 + ring-offset-2)",
      "Keyboard navigable: sidebar, tabs, dialogs, drawers",
      "Map controls must have aria-labels",
      "Reduced motion support"
    ],
    "focus_style": "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[hsl(var(--focus-ring))] focus-visible:ring-offset-2 focus-visible:ring-offset-background",
    "touch_targets": {
      "default": "min-h-[44px]",
      "emergency": "min-h-[56px]"
    }
  },

  "performance": {
    "images": [
      "Use responsive sizes; lazy-load below fold",
      "Prefer WebP when possible",
      "Use skeleton.jsx for loading states"
    ],
    "maps": [
      "Avoid heavy shadows over map tiles",
      "Cluster pins at low zoom",
      "Debounce search/filter updates"
    ]
  },

  "image_urls": {
    "hero_himalayas": [
      {
        "url": "https://images.pexels.com/photos/9275921/pexels-photo-9275921.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "usage": "Landing hero background (cropped, with subtle overlay)"
      },
      {
        "url": "https://images.pexels.com/photos/25490311/pexels-photo-25490311.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "usage": "Featured city section / Explore empty state"
      }
    ],
    "trekking_and_villages": [
      {
        "url": "https://images.pexels.com/photos/25490313/pexels-photo-25490313.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "usage": "Nepal Intelligence hub header (trekking + culture)"
      },
      {
        "url": "https://images.pexels.com/photos/19279803/pexels-photo-19279803.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "usage": "Trip Planner empty state / onboarding illustration substitute"
      }
    ]
  },

  "libraries_and_setup": {
    "recommended": [
      {
        "name": "framer-motion",
        "why": "Premium motion + micro-interactions",
        "install": "npm i framer-motion"
      },
      {
        "name": "recharts",
        "why": "Budget breakdown charts",
        "install": "npm i recharts"
      },
      {
        "name": "lucide-react",
        "why": "Icons (no emoji icons)",
        "install": "npm i lucide-react"
      }
    ],
    "leaflet_notes": [
      "Use custom marker icons that match category colors.",
      "Ensure map controls have sufficient contrast in dark mode (wrap in Card-like container)."
    ]
  },

  "instructions_to_main_agent": {
    "implementation_priorities": [
      "1) Replace index.css tokens with the provided semantic tokens (light + dark).",
      "2) Implement App Shell: desktop sidebar + mobile bottom tabs + top utility row.",
      "3) Build CityBrain Chat: streaming thread + composer + decision cards rail.",
      "4) Build Explore: resizable split view (desktop) + drawer bottom sheet (mobile) + filter chips.",
      "5) Build Emergency Mode with high-contrast, large tap targets.",
      "6) Ensure every interactive element and key info has data-testid (kebab-case)."
    ],
    "js_file_note": "Project uses .js (not .tsx). All component examples should be implemented in .jsx/.js with named exports for components and default exports for pages.",
    "testing_note": "Add data-testid to: nav items, toggles, chat input/send, filters, place cards, save buttons, emergency call buttons, and any critical status banners (offline, location permission)."
  },

  "appendix_general_ui_ux_design_guidelines": "<General UI UX Design Guidelines>\n    - You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms\n    - You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text\n   - NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json\n\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. \n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals.\n</General UI UX Design Guidelines>"
}
