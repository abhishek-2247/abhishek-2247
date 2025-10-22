import requests
import os
from datetime import datetime

USERNAME = "abhishek-2247"
TOKEN = os.getenv("GH_TOKEN").strip()
README_PATH = "README.md"

headers = {"Authorization": f"token {TOKEN}"}
url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"

repos = requests.get(url, headers=headers).json()

table_lines = ["| Repository | Description | Language | Updated |",
               "|-----------|-------------|----------|---------|"]

for repo in sorted(repos, key=lambda x: x["updated_at"], reverse=True):
    name = f"[**{repo['name']}**]({repo['html_url']})"
    desc = repo['description'] or "-"
    lang = repo['language'] or "-"
    updated = datetime.strptime(repo['updated_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
    table_lines.append(f"| {name} | {desc} | {lang} | {updated} |")

with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

start = "<!-- REPO_TABLE_START -->"
end = "<!-- REPO_TABLE_END -->"

new_content = content.split(start)[0] + start + "\n\n" + "\n".join(table_lines) + "\n\n" + content.split(end)[1]

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)
