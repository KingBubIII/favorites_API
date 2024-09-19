from settings import URL_INFO_PATH
from json import load, dumps
from django.shortcuts import render

def docs_view(request):
    url_info = load(open(URL_INFO_PATH))

    # for url, details in url_info.items():
    #     for example in details["examples"]:
    #         for code, response in example["responses"].items():
    #             test = dumps(response, indent=2)
    #             example[code] = test

    context = {}
    context["urls"] = url_info["url_info"]

    return render(request, "url_info.html", context)

def example(request, url_key):
    url_info_file = load(open(URL_INFO_PATH))

    examples = url_info_file["examples"]

    context = {"example":examples[url_key]}

    return render(request, 'example.html', context)