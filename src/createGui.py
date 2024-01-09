import tkinter as tk

def create_gui(toggle_trigger, update_trigger_key, toggle_esp, toggle_defuse):
    root = tk.Tk()
    root.title("Cs2 Cheat")

    # Style
    root.configure(bg="#303030")
    root.geometry("300x200")

    toggle_button = tk.Button(root, text="Toggle Trigger Bot", command=toggle_trigger, bg="#4CAF50", fg="white")
    toggle_button.pack(pady=10)

    esp_button = tk.Button(root, text="Toggle ESP", command=toggle_esp, bg="#FF5722", fg="white")
    esp_button.pack(pady=10)

    defuse_button = tk.Button(root, text="Toggle Defuse Bot", command=toggle_defuse, bg="#03A9F4", fg="white")
    defuse_button.pack(pady=10)

    status_label = tk.Label(root, text="Status: Inactive", bg="#303030", fg="white")
    status_label.pack(pady=5)

    key_label = tk.Label(root, text="Trigger Key:", bg="#303030", fg="white")
    key_label.pack()

    key_entry = tk.Entry(root)
    key_entry.pack(pady=5)

    update_key_button = tk.Button(root, text="Update Key", command=lambda: update_trigger_key(key_entry.get()), bg="#FFC107", fg="black")
    update_key_button.pack(pady=5)

    return root, status_label