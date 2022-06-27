from tkinter import *
from skladopodil_new import *


def get_division():
    word = text.get()
    for item in word:
        symbols = " ,./!@#$%^&*()_=+*<>:;'|[]{}\"0123456789#$~^&*№"
        if item in symbols:
            label['text'] = 'ERROR'
            label.pack()
            return None
    last_list = full_syllable_division(word)
    final_list = formulae_maker(word)
    base_word = final_list[0].lower()
    formulae_word = final_list[1]
    last_list_str = str.join(' - ', last_list)
    label['text'] = base_word + '  :  ' + formulae_word + '  :  ' + last_list_str
    text.delete(0,len(word))

#def onclick(event):
root = Tk()
root.title('SKLADOPODIL')
root.bind('<Return>', lambda x: get_division())
root.geometry('1000x350')
label1=Label(root, text='Введіть слово, яке потрібно розібрати:', font=(18))
label2=Label(root, text=' ')
button = Button(root, text='Divide', font=(14), width=30, height='10')
button.bind('<Button-1>', lambda x: get_division())

label = Label(root, text='', font=('Arial', 24))
text = Entry(root, width=50, font=(18))
text.insert(END, '')


label1.pack()
text.pack()
label2.pack()
button .pack()
label.pack()
root.mainloop()