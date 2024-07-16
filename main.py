import threading
import dearpygui.dearpygui as dpg
from src.createGui import *
from src.triggerBot import TriggerBot
from src.bhopBot import bhopBot
from src.espBot import CS2Esp
from src.noFlash import NoFlash
from src.offsetDumper import *

def main():
    OffsetDumper.fetch_and_set_offsets()
    trigger_bot = TriggerBot()
    esp_bot = CS2Esp()
    bhop_bot = bhopBot()
    no_flash = NoFlash()

    def toggle_all():
        toggle_trigger()
        toggle_esp()
        toggle_noflash()
        toggle_bhop()
        set_status_text(status_label, "All Features: Toggled")

    def toggle_trigger():
        trigger_bot.toggle()
        if trigger_bot.active:
            set_status_text(status_label, "Trigger: Active")
            threading.Thread(target=trigger_bot.run, daemon=True).start()
        else:
            dpg.set_value(status_label, "Trigger: Inactive")

    def toggle_esp():
        if not esp_bot.active:
            esp_bot.toggle()
            set_status_text(status_label, "ESP: Active")
            threading.Thread(target=esp_bot.run, daemon=True).start()
        else:
            esp_bot.toggle()
            set_status_text(status_label, "ESP: Inactive")


    def toggle_noflash():
        no_flash.toggle()
        if no_flash.active:
            set_status_text(status_label, "NoFlash: Active")
            threading.Thread(target=no_flash.run, daemon=True).start()
        else:
            set_status_text(status_label, "NoFlash: Inactive")

    def toggle_bhop():
        bhop_bot.toggle()
        if bhop_bot.active:
            set_status_text(status_label, "Bhop: Active")
            threading.Thread(target=bhop_bot.run, daemon=True).start()
        else:
            dpg.set_value(status_label, "Bhop: Inactive")

    def update_trigger_key(new_key, trigger_bot):
        if new_key and isinstance(new_key, str) and len(new_key) == 1:
            trigger_bot.set_trigger_key(new_key)
            set_status_text(status_label, f"Trigger key updated to: {new_key}")
        else:
            set_status_text(status_label, "Invalid key provided")

    def update_esp_config(setting, value):
        if setting == "box":
            esp_bot.show_box = value
        elif setting == "health":
            esp_bot.show_health = value
        elif setting == "name":
            esp_bot.show_name = value
        elif setting == "skeleton":
            esp_bot.show_skeleton = value
        elif setting == "head":
            esp_bot.show_head = value

    status_label = create_gui(toggle_trigger, update_trigger_key, toggle_esp, toggle_noflash, update_esp_config, toggle_bhop, trigger_bot, toggle_all)

    dpg.start_dearpygui()

if __name__ == '__main__':
    main()
