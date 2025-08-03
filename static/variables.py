from data_storage.json_functions import load_json


data_path = "/home/woniw/Desktop/winow_bot/data_storage/data.json"

data = load_json(data_path)


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"


#! ingredient price dict

ingredient_price = {
    "Flour": 1,
    "Water": 1,
    "Yogurt": 1,
    "Meat": 1
}
