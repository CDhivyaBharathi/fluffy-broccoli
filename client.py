import socket
from threading import Thread
from tkinter import *

#nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class myclients():
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()
        self.login = Toplevel()
        self.login.title("Login")
        self.login.configure(width=500,height=500)
        self.login.resizable(width=False,height=False)

        self.title_msg = Label(self.login,text=" Please login to continue ",justify=CENTER,font='calibiar 20 bold')
        self.title_msg.place(relx=0.2,rely=0.2)

        self.name_label = Label(self.login,text="Name: ",font='calibri 14 bold')
        self.name_label.place(relx=0.1,rely=0.4)

        self.name_box = Entry(self.login,font='calibri 14')
        self.name_box.place(relx=0.3,rely=0.4,relwidth=0.5,relheight=0.05)
        self.name_box.focus()

        self.log_button = Button(self.login,text="Login",font="calibri 20 bold",command=lambda:self.chatwin_go(self.name_box.get()))
        self.log_button.place(relx=0.4,rely=0.6)


        self.window.mainloop()

    

    def chatwin_go(self,name):
        self.login.destroy()
        self.chatwindow(name)
        recieve = Thread(target=self.receive)
        recieve.start()
        
    def chatwindow(self,name):
        self.name = name
        self.window.deiconify()
        self.window.title("Chat screen")
        self.window.configure(width=500,height=500,bg='white')
        self.window.resizable(width= False,height=False)

        self.cli_name = Label(self.window,text=self.name,font='calibri 15 bold',fg='black')
        self.cli_name.place(relx=0.4,rely=0.01)

        self.msg_box = Text(self.window,width=20,height=1,bg='grey',fg='white',font='comicsans 10',padx=5,pady=5)
        self.msg_box.place(relwidth=1,relheight=0.65,rely=0.1)
        self.msg_box.config(cursor= "arrow")

        scroll_bar = Scrollbar(self.msg_box)
        scroll_bar.place(relheight=1,relwidth=0.05,relx=0.95)
        scroll_bar.config(command=self.msg_box.yview)

        

        self.entry_msg = Entry(self.window,bg='grey')
        self.entry_msg.place(rely=0.75,relwidth=1,relheight=0.1)

        self.send_button = Button(self.window,text='SEND',bg='grey',fg='black',font='calibri 20',command=lambda:self.sendButton(self.entry_msg.get()))
        self.send_button.place(relx=0.4,rely=0.85)
        self.msg_box.config(state= DISABLED)

    def sendButton(self,msg):
        self.msg_box.config(state=NORMAL)
        self.msg = msg
        self.entry_msg.delete(0,END)
        mysend = Thread(target = self.write)
        mysend.start()

    def show_message(self,mesg):
        self.msg_box.config(state=NORMAL)
        self.msg_box.insert(END,mesg+"\n")
        self.msg_box.config(state=DISABLED)
        self.msg_box.see(END)
        
    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode("utf-8")
                print("Message: ",message)
                if message == "NICKNAME":
                    client.send(self.name.encode("utf-8"))
                else:
                    self.show_message(message)
            except:
                print("An error occured")
                client.close()
                break

    def write(self):
        self.msg_box.config(state=DISABLED)
        while TRUE:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode("utf-8"))
            self.show_message(message)
            break


gen_client = myclients()



