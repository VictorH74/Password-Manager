import tkinter as tk
import characters as char
from random import choice, randint, shuffle
from tkinter import messagebox as mb # PARA CRIAÇÃO DE POP-UPS
import pyperclip # -> MODULO PARA FUNÇÕES DO CLIPBOARD DE COPIAR/COLAR (copy/paste)
import json


# PASSWORD GENERATOR
def generate_password():
    
    def reset_properties():
        bt_generate_pass.config(text="Generate Password", bg="#D3D3D3")
    
    password_all_char = [choice(char.all_characters) for i in range(randint(6, 10))]
    password_numbers = [choice(char.numbers) for i in range(randint(2, 3))]
    password_symbols = [choice(char.symbols) for i in range(randint(3, 5))]
    
    password_list = password_all_char + password_numbers + password_symbols
        
    shuffle(password_list) # -> ALTERAR ALEATORIAMENTE A POSIÇÃO DE CADA CARACTERE DA VARIAVEL
    
    password = "".join(password_list) # -> PRATICAMENTE MESMA FUNÇÃO QUE O CODIGO COMENTADO ABAIXO
    
    #password = ""
    #for c in password_list:
    #    password += c
    
    password_input.delete(0, tk.END)
    password_input.insert(0, password)
    
    pyperclip.copy(password) # -> METODO PARA COPIAR TEXTO AUTOMATICAMENTE
    
    bt_generate_pass.config(text="Password was copied", bg="#90EE90")
    
    window.after(2000, reset_properties)
    

# SAVE PASSWORD
def add():
    website = website_input.get().title()
    
    email = email_combobox.get()
    if email.count(".com") == 0 or email.count(" ") > 0:
        raise mb.showerror("Error", "the email field was not filled in correctly")
    if email not in emails_list:
        with open("emails.txt", "a") as emails:
            emails.write(f"{email}\n")
        emails_list.append(email)
        email_combobox.config(values=emails_list)
        
    username = user_input.get()
    password = password_input.get()
    
    data_dict = {
        email:{
            website:{
                "User": username,
                "Password": password
            }
        }
    }
    
    if len(website) == 0 or len(password) == 0:
        mb.showerror(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("Passwords.json") as data_file:
                data = json.load(data_file)
                
        except FileNotFoundError:
            with open("Passwords.json", "w") as data_file:
                json.dump(data_dict, data_file, indent=4)
        else:
            try:
                data[email][website] = data_dict[email][website]
            except KeyError:
                data[email] = data_dict[email]
            with open("Passwords.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            user_input.delete(0, tk.END)
            user_input.insert(0, "None")     
            website_input.delete(0, tk.END)
            password_input.delete(0, tk.END)
        
        mb.showinfo(title="Success", message="Password has been saved successfully")
        
        
# SEARCH DATA EMAIL
def search_email():
    email = email_combobox.get()
    if len(email) == 0:
        mb.showwarning("Empty Field", 'the "email" field cannot be empty')
    else:
        items = ""
        try:
            with open("Passwords.json") as file_data:
                data_search = json.load(file_data)
                
                for (key, value) in data_search[email].items():
                    items += f"{key}\n"
                    for (k, v) in value.items():
                        items += f"--> {k}: {v}\n"
                    items += "\n"
                    
        except KeyError:
            mb.showerror("Email Not Found", "the selected email does not exist!")
        except FileNotFoundError:
            mb.showerror('Error', 'No password has been registered!')
        else: 
            mb.showinfo(title=email, message=items)


# UI SETUP
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="#A9A9A9")
window.maxsize(width=800, height=700)

logo = tk.PhotoImage(file="logo.png")

# Canvas
container_img = tk.Canvas(width=200, height=200, bg="#A9A9A9", highlightthickness=0)
container_img.create_image(100, 100, image=logo)
container_img.grid(column=1, row=0)

# Labels
email_label = tk.Label(text="Email:", bg="#A9A9A9", pady=2)
email_label.grid(column=0, row=1, sticky="e")

user_label = tk.Label(text="Username:", bg="#A9A9A9", pady=2)
user_label.grid(column=0, row=2, sticky="e")

website_label = tk.Label(text="Website:", bg="#A9A9A9", pady=2)
#website_label.bind('<Enter>', lambda e: website_label.configure(text='Moved mouse inside'))
#website_label.bind('<Leave>', lambda e: website_label.configure(text='Website'))
website_label.grid(column=0, row=3, sticky="e") # sticky="e" -> GRUDAR NO LADO LESTE(east)

password_label = tk.Label(text="Password:", bg="#A9A9A9", pady=2)
password_label.grid(column=0, row=4, sticky="e")


# Combobox
try:
    with open("emails.txt") as file_emails:
        data_emails = file_emails.readlines() # -> LISTA DE VALORES PARA COMBOBOX
except FileNotFoundError:
    with open("emails.txt", "w") as file_emails:
        pass
    with open("emails.txt") as file_emails:
        data_emails = file_emails.readlines()

emails_list = [email.strip() for email in data_emails]
from tkinter import ttk
emails = tk.StringVar() # -> TIPO DE VALOR QUE SERÁ ARMAZENADO NO COMBOBOX
email_combobox = ttk.Combobox(textvariable=emails, width=29) # -> CRIANDO OBJ COMBOBOX
#email_list = ['vyctor7410@gmail.com', 'victorh.almeida7@gmail.com', 'vyctorh49@gmail.com']
email_combobox.config(values=emails_list) # -> APLICAR LISTA AO COMBOBOX
if len(emails_list) > 0:
    email_combobox.current(0) # -> DEFINIR VALOR NA POSIÇÃO (0) COMO SELECIONADO
email_combobox.grid(column=1, row=1, sticky="w")


# Entries
user_input = tk.Entry()
user_input.insert(0, "None")
user_input.grid(column=1, row=2, columnspan=2, sticky="we")

website_input = tk.Entry()
website_input.focus() # FOCAR NO INPUT AUTOMATICAMENTE PARA DIGITAR SEM PRECISAR USAR O MOUSE
website_input.grid(column=1, row=3, columnspan=2, sticky="ew")  # sticky="ew" -> GRUDAR NOS LADOS LESTE(east) E OESTE(west)

#user_input = tk.Entry()
#user_input.insert(0, "vyctor7410@gmail.com") # 1° PARAM: POSIÇÃO(0 -> INICIO / END -> FINAL) / 2° PARAM: PLACEHOLDER

password_input = tk.Entry(width=32)
password_input.grid(column=1, row=4, sticky="w")


# Buttons
bt_search = tk.Button(text="Search", bg="#D3D3D3", activebackground="#A9A9A9", command=search_email)
bt_search.grid(column=2, row=1, sticky="we")

bt_generate_pass = tk.Button(text="Generate Password", bg="#D3D3D3", width=17, command=generate_password, activebackground="#A9A9A9")
bt_generate_pass.grid(column=2, row=4)

bt_add = tk.Button(text="Add", command=add, bg="#D3D3D3", activebackground="#A9A9A9")
bt_add.grid(column=1, row=5, columnspan=2, sticky="we")




window.mainloop()