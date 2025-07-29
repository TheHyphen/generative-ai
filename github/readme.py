import requests


def download(repo):
    r = requests.get(
        f"https://api.github.com/repos/{repo}/contents/README.md",
        headers={"Accept": "application/vnd.github.raw+json"},
    )
    return r.text
