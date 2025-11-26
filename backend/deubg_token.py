import os
from dotenv import load_dotenv
import httpx

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

print("-" * 30)
if not token:
    print("ERROR: GITHUB_TOKEN is missing from environment!")
else:
    print(f"Token loaded: Yes")
    print(f"Length: {len(token)} chars")
    print(f"First 4: '{token[:4]}'")
    print(f"Last 4:  '{token[-4:]}'")
    
    if token.startswith('"') or token.endswith('"'):
        print("\n[WARNING] Your token has quotes around it! Remove them in .env.")
    if token.startswith(' ') or token.endswith(' '):
        print("\n[WARNING] Your token has leading/trailing spaces! Remove them.")

    print("\nTesting API connection...")
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {token.strip()}"
    }
    try:
        r = httpx.get("https://api.github.com/user", headers=headers)
        print(f"Status Code: {r.status_code}")
        if r.status_code == 200:
            print("SUCCESS: Token is valid!")
            print(f"Authenticated as: {r.json().get('login')}")
        elif r.status_code == 401:
            print("FAILURE: 401 Unauthorized.")
            print("Possible reasons:")
            print("1. The token string is wrong.")
            print("2. SSO (SAML) is enforced by your org and you haven't authorized the token.")
        else:
            print(f"Response: {r.text}")
    except Exception as e:
        print(f"Connection failed: {e}")
print("-" * 30)