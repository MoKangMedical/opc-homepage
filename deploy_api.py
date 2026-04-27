#!/usr/bin/env python3
"""Deploy index.html to GitHub Pages via API (bypasses git proxy issues)"""
import http.client, json, base64, subprocess, os

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = "MoKangMedical/opc-homepage"
BRANCH = "main"

# Get token
result = subprocess.run(
    ['git', 'credential', 'fill'],
    input='protocol=https\nhost=github.com\n',
    capture_output=True, text=True
)
token = None
for line in result.stdout.split('\n'):
    if line.startswith('password='):
        token = line.split('=', 1)[1].strip()
        break

if not token:
    print("ERROR: Could not get GitHub token")
    exit(1)

headers = {
    "Authorization": "token " + token,
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "HermesAgent"
}

def github_api(method, path, data=None):
    conn = http.client.HTTPSConnection("api.github.com")
    h = dict(headers)
    if data:
        h["Content-Type"] = "application/json"
        body = json.dumps(data)
    else:
        body = None
    conn.request(method, path, body=body, headers=h)
    resp = conn.getresponse()
    result = json.loads(resp.read().decode())
    conn.close()
    return result

def upload_file(repo_path, local_path, message):
    with open(local_path, "rb") as f:
        content = f.read()
    
    # Check if file exists
    check = github_api("GET", "/repos/%s/contents/%s" % (REPO, repo_path))
    
    data = {
        "message": message,
        "content": base64.b64encode(content).decode(),
    }
    if "sha" in check:
        data["sha"] = check["sha"]
    
    resp = github_api("PUT", "/repos/%s/contents/%s" % (REPO, repo_path), data)
    if "content" in resp:
        return True
    else:
        print("ERROR uploading %s: %s" % (repo_path, resp.get("message", "unknown")))
        return False

# Upload files
files = [
    ("index.html", "index.html", "Update homepage"),
    ("data.json", "data.json", "Update project data"),
]

for repo_path, local_path, msg in files:
    full_path = os.path.join(BASE, local_path)
    if os.path.exists(full_path):
        print("Uploading %s..." % local_path)
        if upload_file(repo_path, full_path, msg):
            print("  OK")
    else:
        print("SKIP: %s not found" % local_path)

print("Deploy complete: https://mokangmedical.github.io/opc-homepage/")
