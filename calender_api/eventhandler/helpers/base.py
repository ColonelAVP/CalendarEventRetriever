import random
import math
from typing import Union

from rest_framework.renderers import JSONRenderer
from django.http.response import HttpResponse
from django.db.models import Model


class JSONResponse(HttpResponse):
    def __init__(self, data: dict, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, **kwargs)


class BadRequestJSONResponse(HttpResponse):
    def __init__(self, data: dict = None, message: str = None, status=400, **kwargs):
        payload = {"code": status}
        if data:
            payload.update({"response": data})
        if message:
            payload.update({"message": message})
        content = JSONRenderer().render(payload)
        print(content)
        kwargs["content_type"] = "application/json"
        super(BadRequestJSONResponse, self).__init__(content, status=status, **kwargs)


class NotFoundJSONResponse(HttpResponse):
    def __init__(
        self, data: dict = None, message: str = None, status_code=404, **kwargs
    ):
        payload = {"code": 404}
        if data:
            payload.update({"response": data})
        if message:
            payload.update({"message": message})
        content = JSONRenderer().render(payload)
        print(content)
        kwargs["content_type"] = "application/json"
        super(NotFoundJSONResponse, self).__init__(
            content, status=status_code, **kwargs
        )


class SuccessJSONResponse(HttpResponse):
    def __init__(self, data=None, message=None, **kwargs):
        payload = {"code": 200}
        if data:
            payload.update({"response": data})
        if message:
            payload.update({"message": message})
        content = JSONRenderer().render(payload)
        print(content)
        kwargs["content_type"] = "application/json"
        super(SuccessJSONResponse, self).__init__(content, status=200, **kwargs)


def get_or_create(model: Model, *args, **kwargs) -> Model:
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return model(*args, **kwargs)
