import customtkinter
import core
import threading
import json
import os

# CONSTANTS
APP_WIDTH = 600
APP_HEIGHT = 420
APP_DIMENSIONS = str(APP_WIDTH) + 'x' + str(APP_HEIGHT)


# global variables
word = ''
cipher = dict()

"""
The lock prevents multiple threads from modifying the data simultaneously, 
ensuring that the operation is safe and consistent.
"""
lock = threading.Lock()


# method that will be used to get the state of the tabview after every toggle. Add it as a command for tabview
def get_tabview_state():
    if tabview.get() == 'Decrypt':
        encrypt_button.configure(text='Decrypt', command=decrypt)
        label.configure(text='')
        error_label.configure(text='')
        # print('state:', tabview.get(), '\n')
    elif tabview.get() == 'Encrypt':
        encrypt_button.configure(text='Encrypt', command=encrypt)
        label.configure(text='')
        error_label.configure(text='')
        # print('state:', tabview.get(), '\n')
    else:
        encrypt_button.configure(text='Decode', command=decode)
        label.configure(text='')
        error_label.configure(text='')


# encryption method
def encrypt():
    threading.Thread(target=_encrypt, daemon=True).start()


def _encrypt():
    global word
    global cipher
    """
    Locks ensure that the logic inside the with lock: block is executed atomically, 
    meaning that no other thread can interrupt it. This makes the program safer and more reliable.
    
    When multiple threads access and modify shared variables (like word and cipher), 
    I risk data corruption or inconsistencies. 
    Using a lock ensures that only one thread can modify these variables at a time, preventing conflicts.
    """
    with lock:
        # 1- before we encrypt and display the encryption value, make sure there is nothing in output_textbox_encrypt
        output_textbox_encrypt.delete('1.0', 'end')
        input_textbox_decrypt.delete('1.0', 'end')

        # 2- get the word from input_textbox_encrypt
        word = input_textbox_encrypt.get('1.0', 'end').strip()      # removes the extra newline
        temp = word     # store a copy in temp

        # 3- encrypt the word and store the word and the cipher_map in our global variables
        if word != '':
            word, cipher = core.encrypt(word)
            # create a new file and write the data into it
            data_dictionary = {temp: cipher}
            # convert the dictionary to a string in order to use the file.write() function
            data_dictionary_string = json.dumps(data_dictionary, indent=4)
            dir_path = os.path.dirname(os.path.abspath(__file__))
            with open(f'{dir_path}/data.json', 'w') as my_file:     # create json file in the same dir as our python
                my_file.write(data_dictionary_string)
        else:
            label.configure(text='Can not encrypt an empty string', text_color='red')
            print('can not encrypt an empty string')

        # 4- update the encrypted word to output_textbox_encrypt and to input_textbox_decrypt
        output_textbox_encrypt.insert('1.0', word)
        input_textbox_decrypt.insert('1.0', word)


# decryption method
def decrypt():
    threading.Thread(target=_decrypt, daemon=True).start()


def _decrypt():
    global word
    global cipher
    with lock:

        # 1- before we decrypt and display the decryption value, make sure there is nothing in output_textbox_decrypt
        output_textbox_decrypt.delete('1.0', 'end')
        decrypted = ''

        # 2- perform the decryption
        # if input_textbox_decrypt has the word that has been encrypted
        if word and cipher:
            # decrypt that word
            if word == input_textbox_decrypt.get('1.0', 'end').strip():
                decrypted = core.decrypt(word, cipher)
            else:
                decrypted = core.decrypt(input_textbox_decrypt.get('1.0', 'end').strip(), cipher)

        else:
            label.configure(text='Must encrypt a word first', text_color='red')
            print('can not decrypt this')

        # 3- show decrypted value in output_textbox_decrypt
        output_textbox_decrypt.insert('1.0', decrypted)


# reset method
def reset():
    input_textbox_encrypt.delete('1.0', 'end')
    output_textbox_encrypt.delete('1.0', 'end')
    input_textbox_decrypt.delete('1.0', 'end')
    output_textbox_decrypt.delete('1.0', 'end')
    # entries are cleared differently
    key_input_entry.delete(0, 'end')
    text_input_decode.delete('1.0', 'end')
    output_textbox_decode.delete('1.0', 'end')
    label.configure(text='')
    error_label.configure(text='')
    cipher.clear()


# function that decodes with key
def decode():
    threading.Thread(target=_decode, daemon=True).start()


def _decode():
    # before we start the process we wanna clear the textboxes
    output_textbox_decode.delete('1.0', 'end')
    error_label.configure(text='')

    # 1- get the word that should be decoded
    word = text_input_decode.get('1.0', 'end').strip()
    # 2- get the json data
    cipher = key_input_entry.get()
    # 3- from the json data, find the first col in the json string
    col_pos = cipher.find(':')
    # create a new dictionary starting from 2 pos form col_pos, till the element before the last
    # to get rid of the extra {}
    cipher = cipher[col_pos+2:-1]       # now cipher is still a string.

    try:
        # convert cipher to a dictionary
        cipher = json.loads(cipher)
        result = core.decrypt(word, cipher)
        output_textbox_decode.insert('1.0', result)
    except:
        # if the template is wrong show this message
        error_label.configure(text='An Error Occured', text_color='red')
        print('can not decode this')


# create the CTk window
app = customtkinter.CTk()
app.geometry(APP_DIMENSIONS)
app.title('Iron Cipher Mark I')
app.resizable(width=False, height=True)

# create a Label that will display error messages to the user
label = customtkinter.CTkLabel(app, pady=5, text='')
label.pack()

# create a tabview
tabview = customtkinter.CTkTabview(master=app,
                                   width=APP_WIDTH // 2,
                                   height=int(APP_HEIGHT * 0.8),
                                   command=get_tabview_state)
tabview.pack()
# add two tabs
tabview.add('Encrypt')
tabview.add('Decrypt')
tabview.add('Decode')

# design the first tab view
input_textbox_encrypt = customtkinter.CTkTextbox(master=tabview.tab('Encrypt'), width=int(APP_WIDTH*0.416), height=int(APP_HEIGHT*0.57))
input_textbox_encrypt.grid(row=0, column=0, padx=10, pady=10)

output_textbox_encrypt = customtkinter.CTkTextbox(master=tabview.tab('Encrypt'), width=int(APP_WIDTH*0.416), height=int(APP_HEIGHT*0.57),
                                                  # state='disabled'
                                                  )
output_textbox_encrypt.grid(row=0, column=1, padx=10, pady=10)


# design the second tab view
input_textbox_decrypt = customtkinter.CTkTextbox(master=tabview.tab('Decrypt'), width=int(APP_WIDTH*0.416), height=int(APP_HEIGHT*0.57))
input_textbox_decrypt.grid(row=0,column=0,padx=10,pady=10)

output_textbox_decrypt = customtkinter.CTkTextbox(master=tabview.tab('Decrypt'), width=int(APP_WIDTH*0.416), height=int(APP_HEIGHT*0.57),
                                                  # state='disabled'
                                                  )
output_textbox_decrypt.grid(row=0, column=1, padx=10, pady=10)

# design the third tabview
key_label = customtkinter.CTkLabel(master=tabview.tab('Decode'), text='Key in JSON Format', font=('Arial', 12), width=int(APP_WIDTH*0.416), text_color='#00ff00')
key_label.pack(pady=3)

key_input_entry = customtkinter.CTkEntry(master=tabview.tab('Decode'))
key_input_entry.pack(pady=3)

key_label = customtkinter.CTkLabel(master=tabview.tab('Decode'), text='Your Text', text_color='#00ff00')
key_label.pack()

text_input_decode = customtkinter.CTkTextbox(master=tabview.tab('Decode'), width=int(APP_WIDTH*0.416), height=int(APP_HEIGHT*0.15))
text_input_decode.pack(pady=5)

result_label = customtkinter.CTkLabel(master=tabview.tab('Decode'), text='Result', text_color='#00ff00')
result_label.pack()

output_textbox_decode = customtkinter.CTkTextbox(master=tabview.tab('Decode'), width=int(APP_WIDTH*0.416), height=int(APP_HEIGHT*0.15))
output_textbox_decode.pack(pady=5)

error_label = customtkinter.CTkLabel(master=tabview.tab('Decode'), text='')
error_label.pack()

# add a frame that will hold the buttons
button_frame = customtkinter.CTkFrame(app, fg_color='transparent')
button_frame.pack()

# add Encrypt button
encrypt_button = customtkinter.CTkButton(button_frame, text='Encrypt', command=encrypt)
encrypt_button.pack(pady=10, padx=10, side='right')

# add reset button
reset_button = customtkinter.CTkButton(button_frame, text='Reset', fg_color='#c0392b', hover_color='#a93226', command=reset)
reset_button.pack(pady=10, padx=10, side='left')

# display the window
app.mainloop()
