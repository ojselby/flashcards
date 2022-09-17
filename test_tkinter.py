import tkinter as tk


def change_label():
    label1.configure(text='edited by other window')
    return

window1 = tk.Tk()
window2 = tk.Tk()
window3 = tk.Tk()

label1 = tk.Label(master=window1, text='This is window 1')
label2 = tk.Label(master=window2, text='This is window 2')
button = tk.Button(master=window2, text='press to change label', command=change_label)
button.pack()
label2.pack()
label1.pack()

print('a')
window3.mainloop()
print('b')
input('type something')

# window1.mainloop()
