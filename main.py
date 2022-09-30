from gui import make_gui
import json


if __name__ == "__main__":

    with open('conf.txt') as file:
        data = file.read()
    config_data = json.loads(data)

    make_gui(config_data)
