from src.handlers.GetCodesHandler import GetNodeParamsHandler
from src.handlers.ModelsHandler import *

app_urls = [
    ("/get-params", GetNodeParamsHandler),
    ("/model/add", AddModelHandler),
]
