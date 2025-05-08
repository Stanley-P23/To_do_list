import os
import json

from datetime import datetime


DATA_FILE = os.path.join('static', 'assets', 'data', 'test.json')


def load_lists():


    #getting today in string
    today = datetime.now()
    today = today.strftime("%Y-%m-%d")



    if not os.path.exists(DATA_FILE):
        # Create the file if it doesn't exist
        with open(DATA_FILE, 'w') as file:
            dictionary = {
                "to_do_lists": [
                    {
                        "list_id": "1",
                        "date_of_creation": today,
                        "tasks": []
                    }
                ]
            }

            json_string = json.dumps(dictionary, indent=4)
            file.write(json_string)

    with open(DATA_FILE, 'r') as file:
        data = json.load(file)

        extra_lists = len(data['to_do_lists']) - 5
        if extra_lists > 0:
            data['to_do_lists'] = data['to_do_lists'][extra_lists:]

    with open(DATA_FILE, 'w') as file:

        print(data)
        json_string = json.dumps(data, indent=4)
        file.write(json_string)

        return data


load_lists()
