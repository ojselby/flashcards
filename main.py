import json
import tkinter as tk
from json import JSONDecodeError


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


def setup_cards():
    blank_data = {
        'new': {},
        'written': {},
        'learnt': [],
        'learning': []
    }
    with open('stored_cards.txt', 'r') as cards_file:
        try:
            data = json.load(cards_file)
        except JSONDecodeError:
            data = blank_data

        if input('type y to delete all cards (anything else to continue)') == 'y':
            data = blank_data

        while input('type y to add a card (anything else to continue)') == 'y':
            front = input('For the front of the card:')
            back = input('For the back of the card:')
            data['new'][front] = back

        with open('stored_cards.txt', 'w') as cards_file:
            cards_file.write(json.dumps(data))
    return


def flashcard_mode():
    with open('stored_cards.txt', 'r') as cards_file:
        data = json.load(cards_file)

        assert not data['written'], 'not setup for flashcard mode, written should be empty'
        assert data['new'], 'no cards to learn!'

    while input("Type y to stop learning") != 'y':
        # adding all cards to learning if just starting or resetting
        '''
        if not data['learnt']:
            data['learning'] = list(data['new'].keys())
        '''

        # if there are no cards left to learn
        if len(data['learning']) == 0:
            if input('all cards learnt, type y to stop learning or anything else to reset') == 'y':
                with open('stored_cards.txt', 'w') as cards_file:
                    cards_file.write(json.dumps(data))
                    return
            else:
                reset_data(data)
                data['learning'] = list(data['new'].keys())

        # getting the card to test on
        front = data['learning'].pop(0)
        back = data['new'][front]

        # testing user on the card
        print(f'the front of the card is - {front}')
        if input('type anything to see the back'):
            pass
        print(f'the back of the card is - {back}')
        if input('type y if you got this correct, anything else if wrong') == 'y':
            data['learnt'].append(front)
        else:
            data['learning'].append(front)

    # storing changes
    with open('stored_cards.txt', 'w') as cards_file:
        cards_file.write(json.dumps(data))
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


def main(setup=False, show=False):
    if setup:
        setup_cards()

    flashcard_mode()

    if show:
        show_cards()
    return


if __name__ == '__main__':
    main(True, True)

# tkinter text box
'''
    frame = tk.Tk()
    frame.title('FlashCard')
    frame.geometry('400x200')


    def printInput():
        inp = inputtxt.get(1.0, "end-1c")
        lbl.config(text="Provided Input: " + inp)


    inputtxt = tk.Text(frame,
                       height=5,
                       width=20)

    inputtxt.pack()

    printButton = tk.Button(frame,
                            text="Submit",
                            command=printInput)
    printButton.pack()

    lbl = tk.Label(frame, text="")
    lbl.pack()
    frame.mainloop()
'''
