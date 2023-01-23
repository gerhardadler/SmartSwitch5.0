import tkinter as tk

root = tk.Tk()
root.title("SmartSwitch 5.0")

def button1_clicked():
    print("Varmen er på")

def button2_clicked():
    print("Varmen er av")

def button3_clicked():
    print("Economy Mode er aktivert/deaktivert")

button1 = tk.Button(root, text="ON",font="Verdana 30 bold", command=button1_clicked)
button1.pack()

button2 = tk.Button(root, text="OFF",font="Verdana 30 bold", command=button2_clicked)
button2.pack()

button3 = tk.Button(root, text="Economy Mode",font="Verdana 30 bold", command=button3_clicked)
button3.pack()

root.mainloop()
