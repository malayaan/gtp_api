import openai
import os
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk, simpledialog
from tkinter.ttk import Combobox, Scrollbar
from tkinter import Text

# Initialize OpenAI API
openai.api_key = ''

def get_model_response(model, question):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ]
        )
        response_content = response['choices'][0]['message']['content']
        return response_content
    except Exception as e:
        return str(e)

def submit_form():
    tab = notebook.nametowidget(notebook.select())
    model = tab_dict[tab]['model'].get()
    question = tab_dict[tab]['question'].get("1.0",'end-1c')
    response = get_model_response(model, question)
    tab_dict[tab]['chat'].configure(state=tk.NORMAL)
    tab_dict[tab]['chat'].insert(tk.END, "You: " + question + "\n", 'question')
    tab_dict[tab]['chat'].insert(tk.END, "AI: " + response + "\n", 'response')
    tab_dict[tab]['chat'].configure(state=tk.DISABLED)
    tab_dict[tab]['question'].delete("1.0", tk.END)

def rename_tab():
    tab = notebook.nametowidget(notebook.select())
    new_name = simpledialog.askstring("Rename Chat", "Enter new name:")
    if new_name:
        notebook.tab(tab, text=new_name)
        

def save_chat():
    tab = notebook.nametowidget(notebook.select())
    chat = tab_dict[tab]['chat'].get("1.0", tk.END)
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:  # If no file is selected
        return
    f.write(chat)
    f.close()

def save_chats():
    for i, tab in enumerate(tab_dict.keys(), start=1):
        chat = tab_dict[tab]['chat'].get("1.0", tk.END)
        with open(f"chat_{i}.txt", "w") as f:
            f.write(chat)

def load_chat():
    f = filedialog.askopenfile(mode='r', defaultextension=".txt")
    if f is None:  # If no file is selected
        return
    chat = f.read()
    f.close()
    add_tab()
    tab = notebook.nametowidget(notebook.select())
    tab_dict[tab]['chat'].configure(state=tk.NORMAL)
    tab_dict[tab]['chat'].delete("1.0", tk.END)
    tab_dict[tab]['chat'].insert(tk.END, chat)
    tab_dict[tab]['chat'].configure(state=tk.DISABLED)


# Create the main window
root = tk.Tk()
root.state('zoomed')  # Full screen by default
root.configure(bg="white")  # White background

save_button = tk.Button(root, text="Save Chat", command=save_chat, bg="#44475a", fg="white")  # dark grey button with white text
save_button.pack()

load_button = tk.Button(root, text="Load Chat", command=load_chat, bg="#44475a", fg="white")  # dark grey button with white text
load_button.pack()

def close_app():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)

# Create a notebook for the tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

tab_dict = {}

def add_tab():
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=f"Conversation {len(tab_dict)+1}")
    tab_dict[tab] = {}
    model_label = tk.Label(tab, text="Model:", bg="white", fg="black")  # Black text
    model_label.pack()
    model_combobox = Combobox(tab, values=[
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-16k-0613",
        "gtp-4"
    ])
    model_combobox.current(0)  # Set the default option to the first one
    model_combobox.pack()
    tab_dict[tab]['model'] = model_combobox

    chat_label = tk.Label(tab, text="Chat History:", bg="white", fg="black")  # Black text
    chat_label.pack()
    chat = Text(tab, height=10, wrap="word", bg="#D3D3D3", fg="black", cursor="arrow", state=tk.DISABLED)  # Light gray chat
    scroll = Scrollbar(tab, command=chat.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    chat.configure(yscrollcommand=scroll.set)
    chat.pack()
    chat.tag_configure('question', foreground='blue')  # Blue color for user's text
    chat.tag_configure('response', foreground='red')  # Red color for AI's text
    tab_dict[tab]['chat'] = chat

    question_label = tk.Label(tab, text="Your question:", bg="white", fg="black")  # Black text
    question_label.pack()
    question = Text(tab, height=3, wrap="word", bg="#D3D3D3", fg="black", cursor="arrow")  # Light gray question
    question.pack()
    question.bind("<Control-c>", lambda e: root.clipboard_clear())
    question.bind("<Control-v>", lambda e: question.insert(tk.INSERT, root.clipboard_get()))
    tab_dict[tab]['question'] = question

    submit_button = tk.Button(tab, text="Submit", command=submit_form, bg="#D3D3D3", fg="black")  # Light gray button with black text
    submit_button.pack()

    rename_button = tk.Button(tab, text="Rename Chat", command=rename_tab, bg="#D3D3D3", fg="black")  # Light gray button with black text
    rename_button.pack()

add_tab_button = tk.Button(root, text="New Chat", command=add_tab, bg="#D3D3D3", fg="black")  # Light gray button with black text
add_tab_button.pack()

# Start the main loop
root.mainloop()
