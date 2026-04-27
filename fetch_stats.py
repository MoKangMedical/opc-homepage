#!/usr/bin/env python3
"""Fetch GitHub stats for all projects in data.json"""
import http.client, json, subprocess, time, urllib.parse, os

BASE = os.path.dirname(os.path.abspath(__file__))

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

ORG = "MoKangMedical"
headers = {
    "Authorization": "token " + token,
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "HermesAgent"
}

def get_repo_stats(repo_name):
    encoded = urllib.parse.quote(repo_name)
    conn = http.client.HTTPSConnection("api.github.com")
    conn.request("GET", "/repos/" + ORG + "/" + encoded, headers=headers)
    resp = conn.getresponse()
    data = json.loads(resp.read().decode())
    conn.close()
    if "message" in data and data["message"] == "Not Found":
        return None
    return {
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "language": data.get("language", ""),
        "updated": data.get("updated_at", "")[:10],
        "topics": data.get("topics", []),
        "size_kb": data.get("size", 0)
    }

with open(os.path.join(BASE, "data.json")) as f:
    data = json.load(f)

repos = set()
for seg in data["segments"]:
    for p in seg["projects"]:
        repos.add(p["repo"])

print("Fetching stats for %d repos..." % len(repos))

stats = {}
errors = []
for i, repo_name in enumerate(sorted(repos)):
    s = get_repo_stats(repo_name)
    if s:
        stats[repo_name] = s
    else:
        errors.append(repo_name)
    if i % 10 == 0 and i > 0:
        print("  [%d/%d] done..." % (i, len(repos)))
    time.sleep(0.25)

with open(os.path.join(BASE, "github_stats.json"), "w") as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

total_stars = sum(s["stars"] for s in stats.values())
total_forks = sum(s["forks"] for s in stats.values())
print("Done: %d found, %d missing, %d total stars, %d total forks" % (len(stats), len(errors), total_stars, total_forks))
if errors:
    print("Missing: " + ", ".join(errors))
