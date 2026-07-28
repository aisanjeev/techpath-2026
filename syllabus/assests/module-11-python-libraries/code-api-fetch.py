"""
API Data Fetching — Module 11 Code Snap
Run: pip install requests
     python code-api-fetch.py
Fetches data from free public APIs and displays results.
"""
import requests
import json


def fetch_github_user(username):
    """Fetch public GitHub profile info."""
    print(f"\n--- GitHub Profile: {username} ---")

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    user = response.json()
    print(f"  Name:         {user.get('name', 'N/A')}")
    print(f"  Bio:          {user.get('bio', 'N/A')}")
    print(f"  Location:     {user.get('location', 'N/A')}")
    print(f"  Public Repos: {user['public_repos']}")
    print(f"  Followers:    {user['followers']}")
    print(f"  Following:    {user['following']}")
    print(f"  Profile:      {user['html_url']}")

    # Fetch repos
    repos_url = f"https://api.github.com/users/{username}/repos?sort=stars&per_page=5"
    repos_response = requests.get(repos_url)

    if repos_response.status_code == 200:
        repos = repos_response.json()
        print(f"\n  Top Repositories:")
        for repo in repos:
            stars = repo["stargazers_count"]
            lang = repo.get("language", "N/A")
            print(f"    {repo['name']:<30} | {stars} stars | {lang}")


def fetch_random_joke():
    """Fetch a random programming joke."""
    print("\n--- Random Joke ---")

    url = "https://official-joke-api.appspot.com/jokes/programming/random"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        jokes = response.json()

        if jokes:
            joke = jokes[0]
            print(f"  {joke['setup']}")
            print(f"  {joke['punchline']}")
    except requests.exceptions.RequestException as e:
        print(f"  Error fetching joke: {e}")


def fetch_country_info(country):
    """Fetch country information."""
    print(f"\n--- Country Info: {country} ---")

    url = f"https://restcountries.com/v3.1/name/{country}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data:
            c = data[0]
            print(f"  Official Name: {c['name']['official']}")
            print(f"  Capital:       {c.get('capital', ['N/A'])[0]}")
            print(f"  Region:        {c['region']}")
            print(f"  Population:    {c['population']:,}")
            print(f"  Languages:     {', '.join(c.get('languages', {}).values())}")
            currencies = c.get("currencies", {})
            for code, info in currencies.items():
                print(f"  Currency:      {info['name']} ({info.get('symbol', code)})")

    except requests.exceptions.RequestException as e:
        print(f"  Error: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("  API DATA FETCHING DEMO")
    print("=" * 50)

    fetch_github_user("torvalds")
    fetch_random_joke()
    fetch_country_info("india")

    print("\n" + "=" * 50)
    print("Done! Try changing the username or country.")
