"""Read-only Instagram API check. Never prints access tokens or response bodies."""
import json, os, sys, urllib.error, urllib.request

token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "").strip()
if not token:
    sys.exit("ERROR: INSTAGRAM_ACCESS_TOKEN GitHub secret is missing or empty.")
request = urllib.request.Request(
    "https://graph.instagram.com/me?fields=id,username,account_type",
    headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
)
try:
    with urllib.request.urlopen(request, timeout=25) as response:
        profile = json.load(response)
except urllib.error.HTTPError as exc:
    print("Instagram check failed: HTTP", exc.code)
    print("Check token validity, app role and Instagram Login permissions. Token was not printed.")
    sys.exit(1)
except Exception as exc:
    print("Instagram check failed:", type(exc).__name__)
    sys.exit(1)
username=profile.get("username","")
account_id=profile.get("id","")
print("Instagram connection successful:", "@" + username if username else "username unavailable")
print("Account ID retrieved:", "yes" if account_id else "no")
print("Account type:",profile.get("account_type","not supplied"))
if username.lower()!="stor.ysketch":
    sys.exit("Account does not match @stor.ysketch. Do not enable auto-publishing.")
if not account_id:
    sys.exit("Account ID missing.")
print("SAFE CHECK PASSED: No post was created.")
