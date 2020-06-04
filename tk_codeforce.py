import tkinter as tk
import pandas as pd
import requests
import json


class UsernameError(Exception):
    """raised if invalid username"""


def get_data():
    username_label = tk.Label(frame, text='user name', width=15)
    username_label.place(x=10, y=100)

    entry = tk.Entry(frame, text='User name')
    entry.place(x=120, y=100)

    submit = tk.Button(frame, text="Enter", width=15, command=lambda: main_gui(entry.get()))
    submit.place(x=300, y=100)


def main_gui(username):
    if not username:
        username = 'Anu2006'

    widgets = []
    user_info_names = ['current_rating', 'current_rank', 'max_rating', 'max_rank']
    resp = get_url(username.replace(' ', '_'))
    cleaned_data = clean_data(resp)
    mul_by_spaces = lambda info: info + (4 - len(info)) * ' '
    if frame.place_slaves():
        for widget in frame.place_slaves():
            widget.destroy()

    if type(cleaned_data) is pd.DataFrame:
        messages = [f'{name}: {mul_by_spaces(repr(info))}'
                    for info, name in zip(get_user_info(cleaned_data), user_info_names)]

        handle = tk.Label(frame, text=f'User: {username}')
        handle.place(x=120, y=140)

        positions = [180, 200, 220, 240]
        for message, y in zip(messages, positions):
            info_label = tk.Label(frame, text=message)
            info_label.place(x=20, y=y)

    else:
        info_label = tk.Label(frame, text='no results')
        info_label.place(x=20, y=180)

    get_data()


def get_url(username):
    url = f'https://codeforces.com/api/user.rating?handle={username}'
    try:
        return requests.get(url).text

    except requests.ConnectionError:
        print('No Connection')
        exit()


# data cleaning
def clean_data(json_data):
    raw_data = json.loads(json_data)
    if raw_data['status'] == 'FAILED':
        raise UsernameError('Invalid username')

    else:
        if 'result' in raw_data:
            return pd.DataFrame(raw_data['result'])

        else:
            return False


def get_user_info(cleaned_data):
    max_index = len(cleaned_data) - 1
    value_ranges = [max_index, max_index, slice(None, None), slice(None, None)]
    categories = ['newRating', 'rank'] * 2

    for value_range, category in zip(value_ranges, categories):
        try:
            if value_range.__class__ == slice:
                yield max(cleaned_data.loc[value_range, category])

            else:
                yield cleaned_data.loc[value_range, category]

        except LookupError:
            yield None


root = tk.Tk()
root.geometry('600x600')
root.title('code-forces user ratings')

frame = tk.Frame(root, bg='#7e3ba8')
frame.place(relx=0.1, rely=0.1, relwidth=0.8,
            relheight=0.8)

welcome = tk.Label(root, text='welcome', relief='solid', width=20, font=('arial', 19, 'bold'))
welcome.place(x=150, y=80)

get_data()

root.mainloop()
