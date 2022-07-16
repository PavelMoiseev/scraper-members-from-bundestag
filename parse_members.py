import requests
from bs4 import BeautifulSoup

def save_members_link(url_address):
    url_list = []
    for i in range(0, 740, 20):
        url = f"{url_address}{i}"

        q = requests.get(url)
        soup = BeautifulSoup(q.content, "html.parser")

        for person in soup.select(".bt-slide-content"):
            person_page_url = person.select_one("a").get("href")
            url_list.append(person_page_url)

    with open("members_url_list.txt", "a") as file:
        for line in url_list:
            file.write(f"{line}\n")

    pass
