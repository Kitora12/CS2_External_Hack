import threading
from src.createGui import create_gui
from src.triggerBot import TriggerBot
from src.defuseBot import DefuseBot
from src.espBot import CS2Esp
from src.offsetDumper import OffsetDumper

def main():
    OffsetDumper.fetch_and_set_offsets()
    trigger_bot = TriggerBot()
    esp_bot = CS2Esp()
    defuse_bot = DefuseBot()

    esp_active = True
    def toggle_trigger():
        trigger_bot.toggle()
        status_label.config(text=f"Trigger Bot: {'Active' if trigger_bot.active else 'Inactive'}")

    def toggle_esp():
        nonlocal esp_active
        esp_active = not esp_active
        status_label.config(text=f"ESP: {'Active' if esp_active else 'Inactive'}")
        if esp_active:
            threading.Thread(target=esp_bot.run, daemon=True).start()

    def toggle_defuse():
        defuse_bot.toggle()
        status_label.config(text=f"Defuse Bot: {'Active' if defuse_bot.active else 'Inactive'}")
        if defuse_bot.active:
            threading.Thread(target=defuse_bot.run, daemon=True).start()
    
    def update_trigger_key(new_key):
        trigger_bot.set_trigger_key(new_key)

    root, status_label = create_gui(toggle_trigger, update_trigger_key, toggle_esp, toggle_defuse)

    threading.Thread(target=trigger_bot.run, daemon=True).start()

    root.mainloop()

if __name__ == '__main__':
    main()
