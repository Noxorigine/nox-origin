"""
nox_ai.py - appel IA gratuit (Groq) partagé par les workflows NØX.

Principes :
- Plusieurs modèles Groq essayés dans l'ordre (repli sur limite atteinte ou erreur serveur).
- Plafonds d'appels et de jetons PAR RUN. Le quota journalier est protégé par les
  réponses 429 de Groq : on passe alors au modèle suivant, puis au gabarit sans IA.
- Tout texte venant d'inconnus est filtré par Llama Prompt Guard avant envoi.
  Si le filtre est indisponible, le texte n'est PAS envoyé (échec fermé).
- Ne lève jamais d'exception : renvoie None, l'appelant garde son gabarit actuel.
- Aucun secret n'est écrit dans les logs.
"""
import os
import re

import requests

API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
MODELS = [
    m.strip()
    for m in os.environ.get(
        "NOX_AI_MODELS",
        "openai/gpt-oss-120b,qwen/qwen3.8-27b,openai/gpt-oss-20b",
    ).split(",")
    if m.strip()
]
GUARD_MODEL = os.environ.get("NOX_AI_GUARD_MODEL", "meta-llama/llama-prompt-guard-2-86m")
MAX_CALLS = int(os.environ.get("NOX_AI_MAX_CALLS_PER_RUN", "3"))
MAX_GUARD_CALLS = int(os.environ.get("NOX_AI_MAX_GUARD_CALLS_PER_RUN", "10"))
MAX_TOKENS_PER_RUN = int(os.environ.get("NOX_AI_MAX_TOKENS_PER_RUN", "6000"))
TIMEOUT = int(os.environ.get("NOX_AI_TIMEOUT_SECONDS", "30"))
