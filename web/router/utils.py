import json
from optparse import Option
from typing import Any , Optional
from fastapi import FastAPI , Request


def custom_reponse(
    http_status,
    data : Optional[Any] = [],
    errors: Optional[Any]= None,
    errorsMessage: Optional[Any]= None):
    res ={
        "http_status": http_status,
        "data": data,
        "errors":errors,
        "errorMessage": errorsMessage
    }
    return res
