from src.handlers.GetCodesHandler import (
    GetCodeAsyncHandler,
    # GetCodeHandler,
)

app_urls = [
        ("/get-codes-async", GetCodeAsyncHandler),
        # ("/get-codes", GetCodeHandler),
    ]