from settings import URL_INFO_PATH
from json import load, dumps
from django.shortcuts import render

def docs_view(request):
    url_info = load(open(URL_INFO_PATH))

    return render(request, "url_info.html", url_info)

def example(request, url_key):
    url_info_file = load(open(URL_INFO_PATH))

    examples = url_info_file["examples"]

    context = {"example":examples[url_key]}

    return render(request, 'example.html', context)