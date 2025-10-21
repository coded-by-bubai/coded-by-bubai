import requests

username = "coded-by-bubai"
theme = "tokyonight"

README_PATH = "README.md"
MARKER_START = "<!-- REPO-CARDS:START -->"
MARKER_END = "<!-- REPO-CARDS:END -->"

def fetch_repos(user):
    url = f"https://api.github.com/users/{user}/repos"
    response = requests.get(url)
    return response.json()

def generate_card_html(repo):
    return f'''
<p align="left">
  <a href="https://github.com/{username}/{repo}">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username={username}&repo={repo}&theme={theme}" />
  </a>
</p>'''.strip()

def update_readme(repo_cards):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(MARKER_START)
    end = content.find(MARKER_END)

    if start == -1 or end == -1:
        raise Exception("Markers not found in README.md")

    new_content = (
        content[:start + len(MARKER_START)]
        + "\n" + repo_cards + "\n"
        + content[end:]
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    repos = fetch_repos(username)
    # Optional: sort by stargazers_count
    repos = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)

    cards = [generate_card_html(repo["name"]) for repo in repos]
    update_readme("\n".join(cards))

if __name__ == "__main__":
    main()
