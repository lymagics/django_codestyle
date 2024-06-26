from pathlib import Path

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path

import yaml


def docs_schema(request: HttpRequest) -> JsonResponse:
    oas_file = Path(__file__).parent.parent.parent.parent / 'oas.yml'
    oas_docs = yaml.safe_load(oas_file.read_text())
    return JsonResponse(oas_docs)


def docs_ui(request: HttpRequest) -> HttpResponse:
    return render(request, 'swagger_ui.html')


urlpatterns = [
    path('schema/', docs_schema, name='schema'),
    path('', docs_ui, name='docs'),
]
