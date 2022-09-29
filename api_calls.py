import requests
import time

# payload_base = "{\"variations\":[{\"price\":{\"amount\":109.98,\"currency_code\":\"USD\"},\"id\":\"62b5ca9efa18ac7f90fd86ce\"}]}"
# print(payload_base)

# LOGS_PATH = "//jeg-api1/API/Transfer/Wish/Outbox/Price/Logs/"
LOGS_PATH = ""
url = "https://merchant.wish.com/api/v3/products/"
payload1 = "{\"variations\":[{\"price\":{\"amount\":"

payload2 = ",\"currency_code\":\"USD\"},\"id\":\"" \

payload3 = "\"}]}"


def price_update(success_list: list, error_list: list, sku_data: any, token: str, current_file: str) -> None:
    """
    API posts for Wish pricing updates.
    :param success_list: list holding successful API calls
    :param error_list: list holding unsuccessful API Calls
    :param sku_data: Pandas DataFrame with all the SKU and corresponding prices
    :param token: auth token for API calls
    :param current_file: the current file being processed
    :return: None
    """
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + token
    }

    for count in range(len(sku_data)):
        product_id = sku_data.productID[count]
        price = sku_data.price[count]
        variation_id = sku_data.variationID[count]
        request_url = f"{url}{product_id}"
        payload = f"{payload1}{price}{payload2}{variation_id}{payload3}"
        print(payload)

        response = requests.request("PUT", request_url, data=payload, headers=headers)
        time.sleep(1)

        print(response)
        if response.ok:
            success_list.append((sku_data.sku[count], sku_data.price[count], response.status_code, time.ctime()
                                 , current_file.split("/")[-1][6:]))
        else:
            error_list.append((sku_data.sku[count], sku_data.price[count], response.status_code, time.ctime()
                               , current_file.split("/")[-1][6:]))

            print_logs(LOGS_PATH, error_list, success_list, "errors")  # logs errors
            print_logs(LOGS_PATH, error_list, success_list, "success")  # logs success


def print_logs(logs_path: str, error_list: list, success_list: list, log_type: str) -> None:
    if log_type == "errors":
        with open(logs_path + "error_log.txt", "a") as file:
            for error in error_list:
                file.write(str(error) + "\n")
    elif log_type == "success":
        with open(logs_path + "success_log.txt", "a") as file:
            for success in success_list:
                file.write(str(success) + "\n")










