import os
import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Define the path to the JSON file relative to the base directory
DATA_FILE = os.path.join('static', 'assets', 'data', 'data.json')




def write_items(items):
    with open(DATA_FILE, 'w') as file:
        json.dump(items, file, indent=4)
def load_lists():


    #getting today in string
    today = datetime.now()
    today = today.strftime("%Y-%m-%d")



    dictionary = {
        "to_do_lists": [

        ]
    }



    if not os.path.exists(DATA_FILE):
        # Create the file if it doesn't exist
        with open(DATA_FILE, 'w') as file:



            write_items(dictionary)

    with open(DATA_FILE, 'r') as file:
        text = file.read()

    if text == "":
        write_items(dictionary)




    # loading data, adding list for today, deleting empty archived lists, deleting if there's more than 5 lists
    with open(DATA_FILE, 'r') as file:


        data = json.load(file)

        if len(data["to_do_lists"]) == 0:


            today_list = {
                "list_id": "1",
                "date_of_creation": today,
                "tasks": []
            }

            data["to_do_lists"].append(today_list)
            write_items(data)

        elif data["to_do_lists"][-1]["date_of_creation"] != today:

            new_id = int(data["to_do_lists"][-1]["list_id"]) + 1

            today_list = {
                "list_id": str(new_id),
                "date_of_creation": today,
                "tasks": []
            }


            data["to_do_lists"].append(today_list)
            write_items(data)

        for list in data["to_do_lists"][:-1]:
            if len(list["tasks"]) == 0:
                data["to_do_lists"].remove(list)


        extra_lists = len(data['to_do_lists']) - 5
        if extra_lists > 0:
            data['to_do_lists'] = data['to_do_lists'][extra_lists:]
        write_items(data)



        return data





@app.route('/')
def index():
    # Read the current list of to-do lists from the JSON file
    data = load_lists()
    to_do_lists = data.get("to_do_lists", [])

    # Select the most recent to-do list if available
    if to_do_lists:
        last_list = to_do_lists[-1]
    else:
        last_list = {"list_id": "", "date_of_creation": "", "tasks": []}

    return render_template('index.html', to_do_lists=to_do_lists, current_list=last_list)


@app.route('/list/<list_id>')
def list_view(list_id):
    # Read the current list of to-do lists from the JSON file
    data = load_lists()
    to_do_lists = data.get("to_do_lists", [])

    # Find the requested to-do list
    current_list = next((l for l in to_do_lists if l["list_id"] == list_id),
                        {"list_id": "", "date_of_creation": "", "tasks": []})

    return render_template('index.html', to_do_lists=to_do_lists, current_list=current_list)


@app.route('/update_order', methods=['POST'])
def update_order():
    # Read the new order from the request
    data = request.json
    order = data.get('order')
    list_id = data.get('list_id')
    if order and list_id:
        # Read the current list of to-do lists
        data = load_lists()
        to_do_lists = data.get("to_do_lists", [])

        # Find the list to update
        for to_do_list in to_do_lists:
            if to_do_list["list_id"] == list_id:
                tasks = to_do_list.get("tasks", [])
                tasks = [tasks[int(i)] for i in order]
                to_do_list["tasks"] = tasks
                break

        # Write the updated list back to the JSON file
        write_items({"to_do_lists": to_do_lists})

    return jsonify(status='success', new_order=tasks)


@app.route('/update_task', methods=['POST'])
def update_task():
    data = request.json
    list_id = data.get('list_id')
    task_index = int(data.get('task_index'))
    action = data.get('action')

    if list_id and action is not None:
        # Read the current list of to-do lists
        data = load_lists()
        to_do_lists = data.get("to_do_lists", [])

        # Find the list to update
        for to_do_list in to_do_lists:
            if to_do_list["list_id"] == list_id:
                tasks = to_do_list.get("tasks", [])
                if action == 'toggle_complete':
                    task = tasks[task_index]
                    task['completed'] = not task.get('completed', False)
                elif action == 'delete':
                    tasks.pop(task_index)
                to_do_list["tasks"] = tasks
                break

        # Write the updated list back to the JSON file
        write_items({"to_do_lists": to_do_lists})

    return jsonify(status='success')


@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    list_id = data.get('list_id')
    content = data.get('content')

    if list_id and content:
        # Read the current list of to-do lists
        data = load_lists()
        to_do_lists = data.get("to_do_lists", [])

        # Find the list to update
        for to_do_list in to_do_lists:




            if to_do_list["list_id"] == list_id:

                tasks = to_do_list.get("tasks", [])
                new_task = {"content": content, "completed": False}
                tasks.append(new_task)
                to_do_list["tasks"] = tasks
                break

        # Write the updated list back to the JSON file
        write_items({"to_do_lists": to_do_lists})

        return jsonify(status='success', task=new_task)

    return jsonify(status='error', message='Invalid list ID or content')


if __name__ == '__main__':
    app.run(debug=True)
