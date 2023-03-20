import requests
from bs4 import BeautifulSoup
from git import Repo  # pip3 install gitpython
import sys
import os

def is_valid_github_username(user):
    user_url = "https://github.com/" + user
    soup = get_website(user_url)

    images = soup.find_all("img")

    if not images:
        print("ERROR: The user does not exist")
        exit(1)
    else:
        return True


def get_website(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')


def clone_repo(git_url):
    repo_dir = git_url.split("/")[4]
    print("Cloning " + git_url + " to " + repo_dir)
    Repo.clone_from(git_url, repo_dir)


def main():
    user = sys.argv[1]

    if is_valid_github_username(user):
        download_dir = user + "/"
        if not os.path.isdir(download_dir) and not os.path.exists(download_dir):
            os.makedirs(download_dir)
        # move to new directory
        os.chdir(download_dir)

        url = 'https://github.com/' + user + "?tab=repositories"

        url_pages = []
        url_pages.append(url)

        while True:
            soup = get_website(url)
            next_page_link = soup.find_all("a", {"class": "next_page"})
            next_page_link_disabled = soup.find_all("span", {"class": "next_page"})
            if next_page_link:
                href = next_page_link[0].get("href")
                url = 'https://github.com/' + href
                url_pages.append(url)
                continue
            elif next_page_link_disabled:
                break

        repos = []
        i = 0
        for page_url in url_pages:
            i += 1
            soup = get_website(page_url)
            repo_href = soup.find_all("a", {"itemprop": "name codeRepository"})
            for codeRepository_url in repo_href:
                url = 'https://github.com' + codeRepository_url.get("href")
                repos.append(url)

        for repo in repos:
            clone_repo(repo)


if __name__ == '__main__':
    main()
