import requests
import os
from datetime import datetime

USERNAME = "abhishek-2247"
TOKEN = os.getenv("GH_TOKEN", "").strip()
README_PATH = "README.md"

headers = {"Authorization": f"token {TOKEN}"}
url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"

repos = requests.get(url, headers=headers).json()

table_lines = ["| 🗂 Repository | 📝 Description | 💻 Language | ⏰ Updated |",
               "|--------------|----------------|------------|------------|"]

for repo in sorted(repos, key=lambda x: x["updated_at"], reverse=True):
    repo_icon = "🤖" if "ai" in repo['name'].lower() else "💡"
    name = f"{repo_icon} [**{repo['name']}**]({repo['html_url']})"
    lang = repo['language'] or "-"
    if lang:
        lang_colors = {
            "Python": "🐍 Python",
            "JavaScript": "✨ JavaScript",
            "TypeScript": "🔷 TypeScript",
            "Java": "☕ Java",
            "PHP": "🐘 PHP",
            "HTML": "🌐 HTML",
            "CSS": "🎨 CSS",
            "C++": "💠 C++",
            "C": "🔹 C",
            "SQL": "🗄 SQL"
        }
        lang = lang_colors.get(lang, lang)
    desc = repo['description'] or "-"
    updated = datetime.strptime(repo['updated_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
    table_lines.append(f"| {name} | {desc} | {lang} | {updated} |")

with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<!--Start-->"
possible_end_markers = ["<!--End-->", "<!--End--->"]

start_idx = content.find(start_marker)
if start_idx != -1:
    end_idx = -1
    used_end = None
    for em in possible_end_markers:
        idx = content.find(em, start_idx)
        if idx != -1:
            end_idx = idx
            used_end = em
            break
    if end_idx != -1 and used_end is not None:
        before = content[: start_idx + len(start_marker)]
        after = content[end_idx : ]  # includes the end marker and everything after
        replacement = "\n\n" + "\n".join(table_lines) + "\n\n"
        new_content = before + replacement + after
    else:
        new_content = content + "\n\n" + "\n".join(table_lines)
else:
    new_content = content + "\n\n" + "\n".join(table_lines)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)
