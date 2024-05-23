import tkinter as tk
from tkinter import simpledialog, messagebox, Menu, ttk, Text
import os
import keyboard

class TextTemplateHolder:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Template Holder")

        self.templates = {}
        self.load_templates()

        self.tree = ttk.Treeview(root, columns=("Title", "Secret"), show='headings')
        self.tree.heading("Title", text="Template Title")
        self.tree.heading("Secret", text="Template Secret")
        self.tree.pack(padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_tree_select)

        self.update_template_treeview()

        self.menu = Menu(root)
        root.config(menu=self.menu)

        options_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Create Template", command=self.create_or_edit_template)

        self.new_template_button = tk.Button(root, text="New Template", command=self.create_or_edit_template)
        self.new_template_button.pack(pady=5)

        self.run_button = tk.Button(root, text="Start Listening", command=self.toggle_listening)
        self.run_button.pack(pady=5)

        self.current_trigger_label = tk.Label(root, text="Current Trigger: !")
        self.current_trigger_label.pack(pady=5)

        self.input_string = ""
        self.listening = False

    def load_templates(self):
        self.templates = {}
        if os.path.exists('templates.txt'):
            with open('templates.txt', 'r') as file:
                for line in file:
                    if line.strip():
                        parts = line.split(': ', 2)
                        if len(parts) == 3:
                            secret, title, body = parts
                            self.templates[secret.strip()] = {'title': title.strip(), 'body': body.strip()}
                        else:
                            print(f"Skipping invalid line: {line}")

    def save_templates(self):
        with open('templates.txt', 'w') as file:
            for secret, data in self.templates.items():
                file.write(f"{secret}: {data['title']}: {data['body']}\n")

    def update_template_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for secret, data in self.templates.items():
            self.tree.insert('', tk.END, values=(data['title'], secret))

    def paste_template(self, secret):
        body = self.templates[secret]['body']
        for _ in range(len(secret) + 1):
            keyboard.send('backspace')
        keyboard.write(body)
        print(f"Pasting template body: {body}")

    def create_or_edit_template(self, secret=None):
        def save_template():
            secret = secret_entry.get().strip()
            if not secret or len(secret) > 8:
                messagebox.showwarning("Warning", "Secret must be 1-8 characters long.")
                return
            title = title_entry.get().strip()
            body = body_text.get("1.0", tk.END).strip()
            if not body or len(body) > 1000:
                messagebox.showwarning("Warning", "Template body must be 1-1000 characters long.")
                return
            self.templates[secret] = {'title': title, 'body': body}
            self.save_templates()
            self.update_template_treeview()
            template_window.destroy()

        def delete_template():
            del self.templates[secret]
            self.save_templates()
            self.update_template_treeview()
            template_window.destroy()

        if secret:
            title = self.templates[secret]['title']
            body = self.templates[secret]['body']
        else:
            secret, title, body = "", "", ""

        template_window = tk.Toplevel(self.root)
        template_window.title("Create/Edit Template")

        tk.Label(template_window, text="Template Secret:").pack()
        secret_entry = tk.Entry(template_window)
        secret_entry.pack()
        secret_entry.insert(0, secret)

        tk.Label(template_window, text="Template Title:").pack()
        title_entry = tk.Entry(template_window)
        title_entry.pack()
        title_entry.insert(0, title)

        tk.Label(template_window, text="Template Body:").pack()
        body_text = Text(template_window, wrap=tk.WORD, height=10)
        body_text.pack()
        body_text.insert(tk.END, body)

        tk.Button(template_window, text="Save Template", command=save_template).pack()
        if secret:
            tk.Button(template_window, text="Delete Template", command=delete_template).pack()

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = selected_item[0]
            secret = self.tree.item(item, "values")[1]
            self.create_or_edit_template(secret)

    def toggle_listening(self):
        self.listening = not self.listening
        if self.listening:
            self.run_button.config(text="Stop Listening")
            self.start_keylogger()
        else:
            self.run_button.config(text="Start Listening")
            self.stop_keylogger()

    def start_keylogger(self):
        self.input_string = ""
        keyboard.unhook_all()
        keyboard.on_press(self.on_key_press)

    def stop_keylogger(self):
        keyboard.unhook_all()

    def on_key_press(self, event):
        if len(event.name) == 1:  # Ignore non-character keys
            self.input_string += event.name
            if len(self.input_string) > 8:
                self.input_string = self.input_string[-8:]
            for secret in self.templates:
                if self.input_string.endswith(secret + '!'):
                    self.paste_template(secret)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextTemplateHolder(root)
    root.mainloop()

