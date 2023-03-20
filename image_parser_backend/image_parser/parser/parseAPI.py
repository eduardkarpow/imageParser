from serpapi import GoogleSearch

from parser.models import Image
from parser.secretFolder.secret import API_KEY


def parse_images(query):
    imageResults = []
    params = {
        "engine": "google",  # search engine. Google, Bing, Yahoo, Naver, Baidu...
        "q": query+" jpg",  # search query
        "tbm": "isch",  # image results
        "num": "100",  # number of images per page
        "ijn": 0,  # page number: 0 -> first page, 1 -> second...
        "api_key": API_KEY,
        # https://serpapi.com/manage-api-key
        # other query parameters: hl (lang), gl (country), etc
    }
    search = GoogleSearch(params)
    images_is_present = True
    while images_is_present:
        results = search.get_dict()  # JSON -> Python dictionary

        # checks for "Google hasn't returned any results for this query."
        if "error" not in results:
            for image in results["images_results"]:
                if image["original"] not in imageResults:
                    im = Image(name=query, url=image["original"], is_accepted=False)
                    im.save()
        images_is_present = False
