import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL="https://www.shl.com/solutions/products/product-catalog/"

headers={
    "User-Agent":"Mozilla/5.0"
}


catalog=[]


def scrape_catalog():

    response=requests.get(
        BASE_URL,
        headers=headers
    )

    soup=BeautifulSoup(
        response.text,
        "html.parser"
    )

    cards=soup.find_all(
        "a",
        href=True
    )

    seen=set()

    for card in cards:

        href=card["href"]

        if "/product-catalog/view/" not in href:
            continue

        title=card.get_text(
            strip=True
        )

        if not title:
            continue

        if title in seen:
            continue

        seen.add(title)

        if not href.startswith(
            "http"
        ):

            href="https://www.shl.com"+href


        description=title

        lower=title.lower()


        test_type="General"


        if any(
            x in lower
            for x in
            ["java","net","sql","python"]
        ):

            test_type="Technical"


        elif any(
            x in lower
            for x in
            ["personality","opq"]
        ):

            test_type="Personality"


        elif any(
            x in lower
            for x in
            ["ability","cognitive"]
        ):

            test_type="Cognitive"


        catalog.append({

            "name":title,
            "url":href,
            "description":description,
            "test_type":test_type

        })



    os.makedirs(
        "data",
        exist_ok=True
    )


    with open(
        "data/shl_catalog.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            catalog,
            file,
            indent=4
        )


    print(
        f"Saved {len(catalog)} assessments"
    )


if __name__=="__main__":

    scrape_catalog()