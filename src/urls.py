from src.handlers.GetCodesHandler import (
    GetNodeParamsHandler,
    AddModelHandler)

app_urls = [
    ("/get-params", GetNodeParamsHandler),
    ("/add-model", AddModelHandler),
]