"""Configurações centralizadas via variáveis de ambiente."""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
OPEN_ROUTER_KEY: str = os.environ.get("OPEN_ROUTER", "")

DEFAULT_MODEL: str = "groq/llama-3.3-70b-versatile"
MAX_TOKENS: int = 4096
