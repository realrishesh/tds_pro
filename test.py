#!/usr/bin/env python3
"""
Quick sanity‑check for an AI Pipe (AI‑Proxy) key.
"""

import os
import json
import requests

# ── CONFIG ─────────────────────────────────────────────────────────────────────
API_KEY  = os.getenv("API_KEY") 
BASE_URL = "https://aipipe.org/v1"          # ← adjust if your proxy URL differs
MODEL    = "gpt-4o-mini"                     # any model the proxy supports
TIMEOUT  = 15                                # seconds
# ───────────────────────────────────────────────────────────────────────────────

def main():
    if not API_KEY or API_KEY.startswith("PASTE"):
        raise SystemExit("⚠️  Please set API_KEY (env AI_PIPE_KEY or hard‑code).")

    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": "Hello! Just a quick key‑check."}
        ],
        "max_tokens": 10,
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print("❌  Network / connection error:", e)
        return

    if r.status_code == 200:
        data = r.json()
        answer = data["choices"][0]["message"]["content"].strip()
        print("✅  API key is **valid**.")
        print("   Model replied:", repr(answer))
    elif r.status_code in (401, 403):
        print("❌  API key rejected (status", r.status_code, ").")
        print("   Response:", r.text[:300], "…")
    else:
        print(f"⚠️  Unexpected status {r.status_code}")
        print("   Response:", r.text[:300], "…")

if __name__ == "__main__":
    main()
