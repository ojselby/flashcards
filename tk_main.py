import json
import tkinter as tk
from json import JSONDecodeError
from tkinter import messagebox

BULGARIAN_ALPHABET = {
    'a': 'а',
    'b': 'б',
    'v': 'в',
    'g': 'г',
    'd': 'д',
    'e': 'е',
    'j': 'ж',
    'z': 'з',
    'i': 'и',
    'y': 'й',
    'k': 'к',
    'l': 'л',
    'm': 'м',
    'n': 'н',
    'o': 'о',
    'p': 'п',
    'r': 'р',
    's': 'c',
    't': 'т',
    '0': 'у',
    'f': 'ф',
    'h': 'х',
    'x': 'ц',
    'c': 'ч',
    'w': 'ш',
    'q': 'щ',
    'u': 'ъ',
    '3': 'ь',
    '2': 'ю',
    '1': 'я'
}
BLANK_DATA = {
        'new': {},
        'written': {},
        'learnt': [],
        'learning': []
    }


def show_cards():
    with open('stored_cards.txt', 'r') as cards_file:
        data = json.load(cards_file)

        for category in ['new', 'written']:
            print(f'{category} cards:')
            cards = data[category]
            for front in cards:
                print(f'{front} - {cards[front]}')
        print(f'learnt - {data["learnt"]}')
        print(f'learning - {data["learning"]}')
    return


def setup_cards(next_mode='flash'):
    def reset():
        with open('stored_cards.txt', 'w') as cards_file:
            cards_file.write(json.dumps(BLANK_DATA))
        return

    def add():
        front = front_entry.get()
        back = back_entry.get()
        with open('stored_cards.txt', 'r') as cards_file:
            try:
                data = json.load(cards_file)
            except JSONDecodeError:
                data = BLANK_DATA

        data['new'][front] = back
        with open('stored_cards.txt', 'w') as cards_file:
            cards_file.write(json.dumps(data))
        return

    def finish():
        setup_window.destroy()
        if next_mode == 'flash':
            flashcard_mode()
        return

    setup_window = tk.Tk()

    reset_frame = tk.Frame(master=setup_window)
    reset_button = tk.Button(master=reset_frame, text='reset cards', command=reset)
    reset_frame.pack()
    reset_button.pack()

    add_frame = tk.Frame(master=setup_window)
    add_frame.pack()

    front_frame = tk.Frame(master=add_frame)
    front_frame.pack()
    front_label = tk.Label(master=front_frame, text='front:')
    front_label.pack()
    front_entry = tk.Entry(master=front_frame)
    front_entry.pack()

    back_frame = tk.Frame(master=add_frame)
    back_frame.pack()
    back_label = tk.Label(master=back_frame, text='back:')
    back_label.pack()
    back_entry = tk.Entry(master=back_frame)
    back_entry.pack()

    add_button = tk.Button(master=add_frame, text='add card', command=add)
    add_button.pack()

    finish_button = tk.Button(master=setup_window, text='start learning', command=finish)
    finish_button.pack()

    setup_window.mainloop()
    return


def flashcard_mode():
    def next_card():
        if len(data['learning']) == 0:
            reset_data(data)
            data['learning'] = list(data['new'].keys())

        front = data['learning'].pop(0)
        word_label.configure(text=f'{front}')
        flip_button.configure(command=lambda: flip_to_back(front))
        right_button.configure(command=lambda: right(front))
        wrong_button.configure(command=lambda: wrong(front))
        done_button.configure(command=lambda: done(front))
        return

    def right(current):
        data['learnt'].append(current)
        next_card()
        return

    def wrong(current):
        data['learning'].append(current)
        next_card()
        return

    def flip_to_back(front):
        word_label.configure(text=data['new'][front])
        flip_button.configure(command=lambda: flip_to_front(front))
        return

    def flip_to_front(front):
        word_label.configure(text=front)
        flip_button.configure(command=lambda: flip_to_back(front))
        return

    def done(front):
        data['learning'].insert(0,f'{front}')
        # storing changes
        with open('stored_cards.txt', 'w') as cards_file:
            cards_file.write(json.dumps(data))

        flash_window.destroy()
        return

    def on_closing():
        if messagebox.askokcancel("Quit", "If you close without pressing done you will lose data?"):
            flash_window.destroy()

    with open('stored_cards.txt', 'r') as cards_file:
        data = json.load(cards_file)

        assert not data['written'], 'not setup for flashcard mode, written should be empty'
        assert data['new'], 'no cards to learn!'

    if len(data['learning']) == 0:
        reset_data(data)
        data['learning'] = list(data['new'].keys())

    front = data['learning'].pop(0)

    flash_window = tk.Tk()

    flash_window.columnconfigure([0, 2], weight=1, minsize=75)
    flash_window.rowconfigure([0, 2], weight=1, minsize=75)
    flash_window.rowconfigure(1, weight=5, minsize=75)
    flash_window.columnconfigure(1, weight=5, minsize=75)
    word_frame = tk.Frame(master=flash_window, bg='white')
    word_label = tk.Label(master=word_frame, text=f'{front}')
    flip_button = tk.Button(master=flash_window, text=f'flip card',
                            command=lambda: flip_to_back(front))
    right_button = tk.Button(master=flash_window, text='right', command=lambda: right(front))
    wrong_button = tk.Button(master=flash_window, text='wrong', command=lambda: wrong(front))
    done_button = tk.Button(master=flash_window, text='done', command=lambda: done(front))
    word_frame.grid(row=1, column=1, sticky='nsew')
    word_label.pack(fill=tk.BOTH, expand=True)
    word_label.configure(bg='white')
    flip_button.grid(row=2, column=1)
    right_button.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)
    wrong_button.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
    done_button.grid(row=0, column=2, sticky='ne')

    flash_window.protocol("WM_DELETE_WINDOW", on_closing)
    flash_window.mainloop()
    return


def reset_data(data):
    data['learnt'] = []
    data['learning'] = []

    # move all cards back into the new category
    for front in data['written']:
        data['new'][front] = data['written']['front']

    data['written'] = {}
    return


def learning_mode():
    return


def main(setup=True):
    if setup:
        setup_cards()

    else:
        flashcard_mode()

    show_cards()
    return


if __name__ == '__main__':
    main()
