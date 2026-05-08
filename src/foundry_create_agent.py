"""
Deploy agent to Azure AI Foundry via REST API.

Usage (from CI or locally):
  python src/foundry_create_agent.py

Environment variables:
  AZURE_AI_FOUNDRY_ENDPOINT  — Full Foundry project endpoint URL

Authentication:
  Uses DefaultAzureCredential (az login locally, or federated identity in CI).
  Install: pip install azure-identity
"""

import json
import os
import re
import sys
import urllib.request


def sanitize_name(name: str) -> str:
    s = re.sub(r"[^a-z0-9-]", "-", name.lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:63] or "agent"


def get_bearer_token() -> str:
    """Get bearer token using DefaultAzureCredential."""
    try:
        from azure.identity import DefaultAzureCredential
        credential = DefaultAzureCredential()
        token = credential.get_token("https://ai.azure.com/.default")
        return token.token
    except ImportError:
        print("ERROR: Install azure-identity: pip install azure-identity")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to get token: {e}")
        sys.exit(1)


def deploy():
    endpoint = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT", "").rstrip("/")
    if not endpoint:
        print("ERROR: Set AZURE_AI_FOUNDRY_ENDPOINT")
        sys.exit(1)

    token = get_bearer_token()

    url = f"{endpoint}/agents?api-version=2025-05-15-preview"
    payload = json.dumps({
        "name": sanitize_name("meeting-assistant2"),
        "description": "A meeting assistant agent that joins virtual meetings, transcribes conversations in real time, extracts action items, assigns owners, sends follow-up summaries, and schedules follow-up meetings when r",
        "definition": {
            "kind": "prompt",
            "model": "gpt-4o",
            "instructions": "A meeting assistant agent that joins virtual meetings, transcribes conversations in real time, extracts action items, assigns owners, sends follow-up summaries, and schedules follow-up meetings when required."
        }
    }).encode()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            print(f"Agent deployed! ID: {data.get('id', 'unknown')}")
            print(f"Name: {data.get('name', '')}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Deploy failed ({e.code}): {body[:300]}")
        sys.exit(1)


if __name__ == "__main__":
    deploy()
