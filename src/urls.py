from src.handlers.GetCodesHandler import (
    GetNodeParamsHandler,
)

app_urls = [
        ("/get-params", GetNodeParamsHandler),
    ]