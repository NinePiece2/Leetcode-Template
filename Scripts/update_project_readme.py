import os
import re
import json
from pathlib import Path
import requests

SRC_DIR = "Solutions"
SITE_README_PATH = Path("Site_README.md")
GITHUB_README_PATH = Path("README.md")
LINK_ICON = "🔗"

CACHE_FILE = Path(".leetcode_cache.json")

# Load cache
if CACHE_FILE.exists():
    with open(CACHE_FILE, "r") as f:
        QUESTION_CACHE = json.load(f)
else:
    QUESTION_CACHE = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(QUESTION_CACHE, f, indent=2)

ROMAN_NUMERALS = {
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
    "xi", "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii", "xix", "xx"
}

def smart_capitalize(word: str) -> str:
    """Capitalize a word unless it's a Roman numeral in lowercase."""
    if word.lower() in ROMAN_NUMERALS:
        return word.upper()
    return word.capitalize()

def fetch_question_details(slug: str):
    """Fetch difficulty and tags from cache or API."""
    if slug in QUESTION_CACHE:
        return QUESTION_CACHE[slug]["difficulty"], QUESTION_CACHE[slug]["tags"]

    url = "https://leetcode.com/graphql"
    query = {
        "query": """
        query getQuestionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            difficulty
            topicTags {
              name
              slug
            }
          }
        }
        """,
        "variables": {"titleSlug": slug},
    }
    try:
        resp = requests.post(url, json=query, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        question = data.get("data", {}).get("question")
        if not question:
            print(f"⚠️ No question data returned for slug: {slug}")
            return "", []
        difficulty = question.get("difficulty", "")
        tags = [tag.get("name") for tag in question.get("topicTags", []) if tag.get("name")]
        QUESTION_CACHE[slug] = {"difficulty": difficulty, "tags": tags}
        save_cache()
        return difficulty, tags
    except Exception as e:
        print(f"❌ Failed to fetch question details for {slug}: {e}")
        return "", []

# MkDocs badge
def difficulty_badge_site(difficulty: str) -> str:
    colors = {"Easy": "#46c6c2", "Medium": "#fac31d", "Hard": "#f8615c"}
    color = colors.get(difficulty, "#9E9E9E")
    if not difficulty:
        return ""
    return f'<span style="background-color:#ffffff1a; color:{color}; padding:2px 6px; border-radius:6px;">{difficulty}</span>'

# GitHub badge
def difficulty_badge_github(difficulty: str) -> str:
    colors = {"Easy": "4c1", "Medium": "f9c851", "Hard": "e05d44"}
    color = colors.get(difficulty, "9e9e9e")
    if not difficulty:
        return ""
    badge_url = f"https://img.shields.io/badge/Difficulty-{difficulty}-{color}.svg"
    return f"![{difficulty}]({badge_url})"

def generate_table_rows(problems, badge_func):
    rows = []
    for slug, number, title, difficulty, tags in problems:
        diff_badge = badge_func(difficulty)
        tags_str = ", ".join(tags)
        solution_link = f"https://leetcode.romitsagu.com/solutions/{number}/"
        icon_md = f"[{LINK_ICON}]({solution_link})"
        rows.append(f"| {title} | {icon_md} | {diff_badge} | {tags_str} |")
    return "\n".join(rows)

def update_readme(readme_path, rows_str):
    """Update the README table; replaces existing table completely, or creates a new one."""
    if not readme_path.exists():
        raise FileNotFoundError(f"{readme_path} does not exist")

    readme_text = readme_path.read_text()
    
    # Match full table: header + separator + any number of rows
    table_pattern = re.compile(
        r'(\| Problem \| Solution \| Difficulty \| Tags \s*\|\n'  # header
        r'\|[-| ]+\|\n)'                                         # separator
        r'(?:\|.*\|\n?)*',                                       # rows
        re.DOTALL
    )

    new_table = (
        "| Problem | Solution | Difficulty | Tags |\n"
        "|---------|---------|------------|------|\n"
        + rows_str + "\n"
    )

    if table_pattern.search(readme_text):
        updated_text = table_pattern.sub(new_table, readme_text)
        print(f"✅ Updated table rows in {readme_path.name}")
    else:
        updated_text = readme_text.strip() + "\n\n" + new_table
        print(f"✅ Added new table in {readme_path.name}")

    readme_path.write_text(updated_text)


def main():
    problems = []

    for folder in sorted(os.listdir(SRC_DIR)):
        folder_path = Path(SRC_DIR) / folder
        if not folder_path.is_dir():
            continue

        match = re.match(r"(\d+)-(.+)", folder)
        if not match:
            continue
        folder_number, slug = match.groups()
        folder_number = str(int(folder_number))
        title = f"{folder_number}. " + " ".join([smart_capitalize(w) for w in slug.split("-")])

        difficulty, tags = fetch_question_details(slug)
        problems.append((slug, folder_number, title, difficulty, tags))

    site_rows = generate_table_rows(problems, difficulty_badge_site)
    github_rows = generate_table_rows(problems, difficulty_badge_github)

    update_readme(SITE_README_PATH, site_rows)
    update_readme(GITHUB_README_PATH, github_rows)

if __name__ == "__main__":
    main()