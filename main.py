import os

from bs4 import BeautifulSoup
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

fiction = os.getenv("FICTION")
non_fiction = os.getenv("NON_FICTION")
popular_subjects = os.getenv("POPULAR_SUBJECTS")

urls = [fiction, non_fiction, popular_subjects]


print(urls)
print(type(urls))

# for url in books_urls:
#     req = requests.get(url)
#     src = req.text
#     with open(f"{url[23:-11]}.html", "w", encoding='UTF-8', newline='') as file:
#         file.write(src)


# with open("non-fiction.html", encoding='UTF-8', newline='') as file:
#     src = file.read()



req = requests.get(popular_subjects)
src = req.text

soup = BeautifulSoup(src, "lxml")

all_products = soup.find_all(class_="image")

items_link = []

for item in all_products:
    items_link.append(item.find('a').get("href"))

books_list = []
i = 1
for item in items_link:
    book = {}
    req = requests.get(item)
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    book["book_title"] = soup.find("h1", id="title-page").text
    book["book_img"] = soup.find("div", class_="item").find("a").get("href")
    book["book_author"] = soup.find("div", class_="description").find("a").text
    book["book_price"] = soup.find("div", class_="price").find("span", id="price-old").text
    book["book_description"] = soup.find("div", id="content").find("div", class_="tab-content").get_text()

    books_list.append(book)
    time.sleep(1)
    print(f"книга {i}")
    i += 1

with open("popular-subjects_books_list.json", "a", encoding='UTF-8', newline='') as file:
    json.dump(books_list, file, indent=4, ensure_ascii=False)
