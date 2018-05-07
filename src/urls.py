from src.handlers.GetCodesHandler import (
    GetCodeAsyncHandler,
    GetNodeParamsHandler,
)

app_urls = [
        ("/get-codes-async", GetCodeAsyncHandler),
        ("/get-params", GetNodeParamsHandler),
    ]