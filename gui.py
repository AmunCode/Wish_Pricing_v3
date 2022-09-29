import tkinter as tk
import requests
import glob
import pandas as pd
import shutil
import time
import api_calls as api

FILE_PATH = "//jeg-api1/API/Transfer/Wish/Outbox/Price/"
DESTINATION_PATH = "//jeg-api1/API/Transfer/Wish/Outbox/Price/Processed/"
# LOGS_PATH = "//jeg-api1/API/Transfer/Wish/Outbox/Price/Logs/"
LOGS_PATH = ""

current_file = ""

for file in glob.glob(FILE_PATH + "e20Wireless_Price*.csv"):
    current_file = file
    print(file)

headers = {
    'content-type': "application/json",
    'authorization': "Bearer 35601379c4e74f9083e0f4a1e10af3b4"
}


def make_gui():
    # open config file to retrieve token, then concatenate for validation
    with open("config.txt") as config_file:
        token = config_file.read()
        token_verification_clone = "Bearer " + token

    # Verify if current token is valid.
    auth_url = "https://merchant.wish.com/api/v3/oauth/test"
    header = {"authorization": token_verification_clone}
    auth_ver_response = requests.request("GET", auth_url, headers=header)

    token_test_payload = {
        "access_token": token
    }

    error_list = []
    success_list = []

    # if the token is valid
    if auth_ver_response.ok:
        with open(LOGS_PATH + "success_log.txt", "a") as success_file:
            success_file.write(f"Authorized: token valid {time.ctime()} \n")

        # JSON to be pushed on each API call
        sku_data = []
        for sku_file in glob.glob(FILE_PATH + "e20Wireless_Price*.csv"):
            sku_data = pd.read_csv(sku_file)  # reads SKU data from file into a pandas dataFrame
            shutil.move(sku_file,
                        DESTINATION_PATH)  # moves SKU file to a different folder once data is loaded

        # calls a function to update the price of each SKU via Wish API.
        api.price_update(success_list, error_list, sku_data, token, current_file)
    else:
        # only executes is the token in the config file is invalid
        with open(LOGS_PATH + "error_log.txt", "a") as error_file:
            error_file.write(
                f"Not authorized: token invalid {time.ctime()} {current_file.split('/')[-1][6:]} \n")

        def get_new_token():
            """
                        collects user token input in GUI
                        :return: None
                        """
            print("get token function reached")
            new_token = input_token.get()
            write_new_token(new_token)

            with open("config.txt") as file:
                new_token = file.read()
                new_token_verification_clone = "Bearer " + new_token

            # Verify if the new token is valid.
            new_token_header = {"authorization": new_token_verification_clone}
            new_auth_ver_response = requests.request("GET", auth_url, headers=new_token_header)

            if new_auth_ver_response:
                display_current_token.configure(text=new_token)
            else:
                display_current_token.configure(text=new_token)
                invalid_msg = tk.Label(text="Invalid token!")
                invalid_msg.configure(fg='red')
                invalid_msg.grid(row=0, column=2)

        def write_new_token(updated_token):
            """
                        Stores token into config.txt file
                        :param updated_token:
                        :return: None
                        """
            with open("config.txt", "w") as file:
                file.write(updated_token)

        def run_manual_api():
            """
                        allows use to trigger a price API update from the GUI
                        :return: None
                        """
            sku_data_manual = []
            # upload the data file
            for file in glob.glob(FILE_PATH + "e20Wireless_Price*.csv"):
                sku_data_manual = pd.read_csv(file)
                shutil.move(file, DESTINATION_PATH)
            # calls API to update prices.
            api.price_update(success_list, error_list, sku_data, token, current_file)

        # Create GUI window.
        window = tk.Tk()
        window.title("Wish Pricing API")
        window.geometry("300x200")

        current_token = tk.Label(text="Current token: ")
        current_token.grid(row=0, column=0)

        display_current_token = tk.Label(text=token_test_payload['access_token'])
        display_current_token.grid(row=0, column=1)

        update_token = tk.Label(text="Update token: ")
        update_token.grid(row=1, column=0)

        input_token = tk.Entry()
        input_token.grid(row=1, column=1)

        update_token_button = tk.Button(text="Update Token", command=get_new_token)
        update_token_button.grid(row=2, column=1)

        run_api_button = tk.Button(text="Push Price Updates", command=run_manual_api)
        run_api_button.grid(row=3, column=1)

        window.mainloop()
