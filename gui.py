from tkinter import Tk, Entry, Button, mainloop, Label, StringVar
from PIL import ImageTk, Image


def start_gui(file):
    def destroy():
        root.destroy();

    root = Tk(className='Enter the captcha', )
    root.attributes("-topmost", True)
    message = StringVar(root)
    img = ImageTk.PhotoImage(Image.open(file))
    view = Label(root, image=img, width=img.width())
    view.pack()
    text_box = Entry(root, textvariable=message)
    text_box.pack()
    button = Button(root, text="Commit", command=lambda: destroy())
    button.pack()
    mainloop()
    return message.get()


if __name__ == '__main__':
    print(start_gui('captcha.png'))
