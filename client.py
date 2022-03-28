from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf-8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def send(event= None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf-8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event= None):
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Just Chatting")
top.geometry("700x360")
top.configure(bg='#4D4D4D')

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Текст..")

scrollbar = tkinter.Scrollbar(messages_frame)


msg_list = tkinter.Listbox(messages_frame,
                           height=15, width=80,
                           yscrollcommand=scrollbar.set,
                           )
scrollbar.configure(command=msg_list.yview)
msg_list.configure(bg='#332956', fg='#64A5CC',
                   relief='solid', font="Times 10 bold",
                   )
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack(pady=20)

Label_1 = tkinter.Label(top,
                        relief ="solid",
                        font="Times 10 bold",
                        padx=50
                        )
enter_fd = tkinter.Entry(Label_1, width=51, textvariable=my_msg,
                         font="Times 10 bold"
                         )
enter_fd.bind("<Return>", send)
Label_1.pack()
enter_fd.pack()

send_button = tkinter.Button(Label_1, text="Отправить", command=send,
                             relief="solid",
                             font="Times 10 bold",
                             bg='#9E9E9E', activebackground="#859D7B", padx=35, pady=3
                             )
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = "127.0.0.1"
PORT = 5050
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()