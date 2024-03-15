import tkinter as tk
from cryptography.fernet import Fernet
import os
import re
import shutil
import subprocess
import json

current_dir = "C:\Code Files\Python\Commandline"

def is_folder_present(parent_folder, target_folder):
    items = os.listdir(parent_folder)
    
    return target_folder in items

command_count = 0

#States
current_state = 0
MAIN_STATE = 0
EDIT_STATE = 1
#Editing
open_file = None

def on_submit(event=None):
    global command_count, current_dir, current_state, open_file
    commands = ["cd", "ls", "exit", "cls", "clear", "mkdir", "createdir", "mkfile", "createfile", "rem", "remove", "read", "readfile", "edit", "editfile", "vol", "volume", "alias", "pwd", "mv", "move"]
    input_text = entry.get("1.0", tk.END).strip()
    parts = input_text.split(">", 1)
    result = parts[1] if len(parts) > 1 else ""
    result = result.lstrip().split(" ")
    
    #Aliases
    aliases = {}
    if os.path.exists("aliases.json"):
        f = open("aliases.json", "r")
        try:
            content = json.load(f)
        except json.decoder.JSONDecodeError:
            content = {}
        
        for alias in content:
            aliases[alias] = content[alias]
            
    for command in commands:
        if command not in aliases:
            aliases[command] = []
    
    #Remove text Widget stuff from ls or whatever
    text_widget.config(state=tk.NORMAL)
    if command_count != 0:
        text_widget.insert(tk.END, "\n\n")
        
    text_widget.insert(tk.END, "Input: " + ' '.join(result) + "\n")
    text_widget.config(state=tk.DISABLED)
    # Parse text
    """if result[0] == "encrypt" or result[0] in aliases["encrypt"]:
        if len(result) < 2:
            edit_wdiget_text("Second arg missing (encrypt [file_name])")
        else:
            edit_wdiget_text(f"Trying to encrypt file: {result[1]}")
            key = Fernet.generate_key()

    el"""
    if result[0] == "cd" or result[0] in aliases["cd"]:
        if len(result) < 2:
            edit_wdiget_text("Second arg missing (cd [folder_name])")
        else:
            parent_folder = current_dir
            target_folder = result[1]

            if(result[1].startswith("\"")):
                complete = ' '.join(result)
                match = re.search(r'"(.*?)"', complete).group(1)
                target_folder = match

            if(target_folder == ".."):
                if(parent_folder != "C:"):
                    current_dir = parent_folder[:parent_folder.rfind("\\")]
                else:
                    result_label.config(text=f"Can't go further than C:\\")
            else:
                if(is_folder_present(parent_folder + "\\", target_folder)):
                    current_dir = current_dir + "\\" + target_folder
                    edit_wdiget_text(f"Now in: \"{target_folder}\"")
                else:
                    edit_wdiget_text(f"Folder \"{target_folder}\" not found!")
    elif result[0] == "ls" or result[0] in aliases["ls"]:

        files = [item for item in os.listdir(current_dir + "\\")]

        edit_wdiget_text('\n'.join(files))
    elif result[0] == "exit" or result[0] in aliases["exit"]:
        root.destroy()
    elif result[0] == "cls" or result[0] == "clear" or result[0] in aliases["cls"] or result[0] in aliases["clear"]:
        command_count = -1
        clear_widget()
    elif result[0] == "mkdir" or result[0] == "createdir" or result[0] in aliases["mkdir"] or result[0] in aliases["createdir"]:
        if(len(result) < 2):
            edit_wdiget_text("Second arg missing (mkdir [new_dir_name])")
        else:
            try:
                os.mkdir(current_dir + "\\" + result[1])
                edit_wdiget_text(f"Created folder {result[1]} in {current_dir}")
            except PermissionError:
                edit_wdiget_text(f"Not enough permissions to create a directory in {current_dir}\. Start an elevated command prompt.")
    elif result[0] == "mkfile" or result[0] == "createfile" or result[0] in aliases["mkfile"] or result[0] in aliases["createfile"]:
        if(len(result) < 2):
            edit_wdiget_text("Second arg missing (mkfile [new_file_name])")
        else:
            try:
                open(f"{current_dir}\\{result[1]}", "w")
                edit_wdiget_text(f"Created file {result[1]} in {current_dir}")
            except PermissionError:
                edit_wdiget_text(f"Not enough permissions to create a file in {current_dir}\. Start an elevated command prompt.")
    elif result[0] == "rem" or result[0] == "remove" or result[0] in aliases["rem"] or result[0] in aliases["remove"]:
        if(len(result) < 2):
            edit_wdiget_text("Second arg missing (rem [item_to_remove])")
        else:
            try:
                shutil.rmtree(result[1])
                edit_wdiget_text(f"Removed item {result[1]} in {current_dir}")
            except PermissionError:
                edit_wdiget_text(f"Not enough permissions to remove an item in {current_dir}\. Start an elevated command prompt.")
            except FileNotFoundError:
                edit_wdiget_text(f"Cannot find file: {result[1]}")
    elif result[0] == "read" or result[0] == "readfile"  or result[0] in aliases["read"] or result[0] in aliases["readfile"]:
        if(len(result) < 2):
            edit_wdiget_text(f"Second arg missing (read [file_to_read])")
        else:
            try:
                output_str = ""

                file = open(f"{current_dir}\\{result[1]}", "r")
                lines = file.readlines()

                for line in lines:
                    output_str += line + "\n"

                edit_wdiget_text(f"{output_str}")
            except FileNotFoundError:
                edit_wdiget_text(f"Cannot find file: {result[1]}")
    elif result[0] == "edit" or result[0] == "editfile"  or result[0] in aliases["edit"] or result[0] in aliases["editfile"]:
        if(len(result) < 2):
            edit_wdiget_text("Second arg missing (edit [file_to_edit])")
        else:
            try:
                entry.delete("1.0", tk.END)
                entry.insert(tk.END, current_dir + "\> ")
                entry.config(state=tk.DISABLED)
                
                clear_widget(True)
                file = open(f"{current_dir}\\{result[1]}", "r")
                lines = file.readlines()

                for line in lines:
                    text_widget.insert(tk.END, line)
                    
                current_state = EDIT_STATE
                open_file = f"{current_dir}\\{result[1]}"

            except FileNotFoundError:
                text_widget.config(state=tk.NORMAL)
                text_widget.config(state=tk.DISABLED)
                edit_wdiget_text("Cannot find file: {result[1]}")
    elif result[0] == "vol" or result[0] == "volume" or result[0] in aliases["vol"]  or result[0] in aliases["volume"]:
        try:
            result = subprocess.run(['vol', 'C:'], shell=True, stdout=subprocess.PIPE, text=True, check=True)
            lines = result.stdout.split("\n")

            output_str = ""

            if lines:
                for line in lines:
                    output_str += line.strip() + "\n"

                edit_wdiget_text(output_str)
            else:
                edit_wdiget_text("Volume Information not found in the output.")

        except subprocess.CalledProcessError:
            edit_wdiget_text("Could not find the current volume. Either the access has been denied or there is a problem with your device.")
    elif result[0] == "alias":
        #alias <old> <new>
        if len(result) == 1:
            if not os.path.exists("aliases.json"):
                f = open("aliases.json", "w")
                f.close()
            f = open("aliases.json", "r")
            content = ""
            try:
                content = json.load(f)
            except json.decoder.JSONDecodeError:
                content = {}
            f.close()
            
            final_str = "(Alias -> Command)"
            for alias in content:
                commands = ', '.join(content[alias])
                
                final_str += f"\n{alias} -> {commands}"
                
            edit_wdiget_text(final_str)
                
        elif(len(result) < 3):
            edit_wdiget_text("Syntax incorrect. <alias <old-name> <new-name>")
        else:
            old_name = result[1]
            new_name = result[2]
            
            if old_name == "alias":
                edit_wdiget_text("You cannot alias this command!")
            elif(old_name not in commands):
                edit_wdiget_text("The command you provided doesn't exist!")
            else:
                if new_name.strip() == "":
                    edit_wdiget_text("This alias is not allowed!")
                else:
                    if not os.path.exists("aliases.json"):
                        f = open("aliases.json", "w")
                        f.close()
                    f = open("aliases.json", "r")
                    content = ""
                    try:
                        content = json.load(f)
                    except json.decoder.JSONDecodeError:
                        content = {}
                    f.close()
                    
                    current_aliases = []
                    
                    if old_name in content and new_name in content[old_name]:
                        edit_wdiget_text(f"You already have {new_name} set as an alias of {old_name}!")
                    else:
                        if old_name in content:
                            current_aliases = content[old_name]
                            current_aliases.append(new_name)
                        else:
                            current_aliases = [new_name]
                        content[old_name] = current_aliases
                    
                        f = open("aliases.json", "w")
                        json.dump(content, f, indent=2)
                        f.close()
                        
                        edit_wdiget_text(f"Alias added: {old_name} now has following aliases: {current_aliases}")
    elif result[0] == "unalias":
        if(len(result) < 2):
            edit_wdiget_text("Syntax incorrect. <alias <old-name> (alias)")
        else:
            original_command = result[1]
            special_alias = ""
            if len(result) > 2:
                special_alias = result[2]
                
            if(original_command not in commands):
                edit_wdiget_text("The command you provided doesn't exist!")
            else:
                if not os.path.exists("aliases.json"):
                    edit_wdiget_text("This command doesn't have an alias!")
                else:
                    f = open("aliases.json", "r")
                    content = ""
                    try:
                        content = json.load(f)
                    except json.decoder.JSONDecodeError:
                        edit_wdiget_text("This command doesn't have an alias!")
                    f.close()
                                            
                    if original_command not in content:
                        edit_wdiget_text("This command doesn't have an alias!")
                    else:
                        aliases = content[original_command]
                        
                        if special_alias == "":
                            del content[original_command]
                            edit_wdiget_text(f"All aliases for \"{original_command}\" removed!")
                        else:
                            if special_alias not in content[original_command]:
                                edit_wdiget_text(f"This command doesn't have the alias: {special_alias}")
                            else:
                                if(len(content[original_command]) == 1):
                                    del content[original_command]
                                    edit_wdiget_text(f"Alias \"{special_alias}\" for {original_command} removed!")
                                else:
                                    content[original_command].remove(special_alias)
                                    edit_wdiget_text(f"Alias \"{special_alias}\" for {original_command} removed!")
                                    
                        f = open("aliases.json", "w")
                        json.dump(content, f, indent=2)
                        f.close()
    elif result[0] == "pwd" or result[0] in aliases["pwd"]:
        edit_wdiget_text(f"{current_dir}")
    elif result[0] == "mv" or result[0] == "move" or result[0] in aliases["mv"] or result[0] in aliases["move"]:
        #mv <old> <new>
        if len(result) < 3:
            edit_wdiget_text("Syntax incorrect. mv <file_name/path> <new_path>")
        else:
            old_path = result[1]
            
            path = ""
            pass_path = True
            
            if(result[1].startswith("\"")):
                complete = ' '.join(result)
                match = re.search(r'"(.*?)"', complete).group(1)
                old_path = match
                joined_data = ' '.join(result)
                joined_data = joined_data.replace(f"\"{match}\"", "placeholder")
                result = joined_data.split(" ")
            
            if len(result) < 3:
                edit_wdiget_text("Syntax incorrect. mv <file_name/path> <new_path>")
            else:
                new_path = result[2]
                
                if(result[2].startswith("\"")):
                    complete = ' '.join(result)
                    match = re.search(r'"(.*?)"', complete)
                    if match != None:
                        match.group(1)
                        new_path = match
                        joined_data = ' '.join(result)
                        joined_data = complete.replace(f"\"{match}\"", "placeholder")
                        result = joined_data.split(" ")
                
                if os.path.exists(old_path):
                    path = old_path
                elif os.path.exists(current_dir + "\\" + old_path):
                    path = current_dir + "\\" + old_path
                else:
                    edit_wdiget_text("Cannot find the file to move! Is the path correct?")
                    pass_path = False
                    
                if pass_path:
                    if not os.path.exists(new_path):
                        edit_wdiget_text("Cannot find the folder to move the file to! Is the path correct?")
                    else:
                        shutil.move(path, new_path)
                        edit_wdiget_text("File moved!")
            
            
    else:
        edit_wdiget_text(f"Unknown command: {result[0]}")

    text_widget.yview(tk.END)
    
    command_count += 1

    # Restore the initial text after processing
    entry.delete("1.0", tk.END)
    entry.insert(tk.END, current_dir + "\> ")

def remove_trailing_empty_lines(lines):
    print(lines)
    lines = lines.splitlines()
    
    while lines and lines[-1].strip() == "":
        lines.pop()
        
    return '\n'.join(lines)

def restore_initial_text():
    initial_text = current_dir + "\> "
    current_text = entry.get("1.0", tk.END).strip()

    if not current_text.startswith(initial_text):
        entry.delete("1.0", tk.END)
        entry.insert(tk.END, initial_text)

    root.after(100, restore_initial_text)

def prevent_editing(event):
    current_index = entry.index(tk.INSERT)
    initial_text_length = len(current_dir + "\> ")

    if int(current_index.split('.')[1]) < initial_text_length:
        return 'break'
    
def exit_current_state(event):
    if event.keysym == "x":
        print(current_state)
        if current_state == EDIT_STATE:
            if open_file == None:
                edit_wdiget_text("Error editing file. Please try again.")
            elif not os.path.exists(open_file):
                edit_wdiget_text("Error editing file. Did it get renamed, moved, or deleted?")
            else:
                content = remove_trailing_empty_lines(text_widget.get("1.0", tk.END))
                f = open(open_file, "w")
                f.write(content)
                f.close()
                
                clear_widget()
                edit_wdiget_text("File saved!")
                entry.config(state=tk.NORMAL)
            
def clear_widget(keep_open=False):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    if not keep_open:
        text_widget.config(state=tk.DISABLED)
        
def edit_wdiget_text(text):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, text)
    text_widget.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Command Line")
root.configure(bg="#1E1E1E")

char_width = 8
char_height = 16
window_width = char_width * 80
window_height = char_height * 25
root.geometry(f"{window_width}x{window_height}")
root.bind('<Control-Key>', exit_current_state)

entry = tk.Text(root, width=40, height=1, font=("Courier", 12), insertbackground="#FFFFFF", fg="#FFFFFF", bg="#1E1E1E", bd=0)
entry.insert(tk.END, "C:\\>")
entry.tag_add("readonly", "1.0", "1.end")
entry.tag_config("readonly", foreground="#FFFFFF", background="#1E1E1E")
entry.bind("<Return>", on_submit)
entry.bind("<Key>", prevent_editing)
entry.pack(side="top", fill="both", expand=True)

scrollbar = tk.Scrollbar(root, command=entry.yview)
scrollbar.pack(side="right", fill="y")

entry.config(yscrollcommand=scrollbar.set)

result_label = tk.Label(root, text="", fg="#FFFFFF", bg="#1E1E1E")
result_label.pack()

text_widget = tk.Text(root, wrap="word", yscrollcommand=lambda *args: scrollbar.set(*args), font=("Courier", 12), fg="#FFFFFF", bg="#1E1E1E", bd=0)
text_widget.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(root, command=text_widget.yview)
scrollbar.pack(side="right", fill="y")
text_widget.config(state=tk.DISABLED)

text_widget.config(yscrollcommand=scrollbar.set)


# Periodically restore the initial text
root.after(100, restore_initial_text)

root.mainloop()