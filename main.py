import threading
import dearpygui.dearpygui as dpg
from src.createGui import *
from src.triggerBot import TriggerBot
from src.bhopBot import bhopBot
from src.espBot import CS2Esp
from src.aimBot import AimBot
from src.defuseBot import DefuseBot
from src.offsetDumper import *

def main():
    OffsetDumper.fetch_and_set_offsets()
    trigger_bot = TriggerBot()
    esp_bot = CS2Esp()
    aim_bot = AimBot()
    bhop_bot = bhopBot()
    defuse_bot = DefuseBot()

    def toggle_trigger():
        trigger_bot.toggle()
        if trigger_bot.active:
            set_status_text(status_label, "Status: Active")
            threading.Thread(target=trigger_bot.run, daemon=True).start()
        else:
            dpg.set_value(status_label, "Status: Inactive")

    def toggle_esp():
        if not esp_bot.active:
            esp_bot.toggle()
            set_status_text(status_label, "ESP: Active")
            threading.Thread(target=esp_bot.run, daemon=True).start()
        else:
            esp_bot.toggle()
            set_status_text(status_label, "ESP: Inactive")


    def toggle_defuse():
        defuse_bot.toggle()
        if defuse_bot.active:
            set_status_text(status_label, "Status: Active")
            threading.Thread(target=defuse_bot.run, daemon=True).start()

    def toggle_bhop():
        bhop_bot.toggle()
        if bhop_bot.active:
            set_status_text(status_label, "Status: Active")
            threading.Thread(target=bhop_bot.run, daemon=True).start()
        else:
            dpg.set_value(status_label, "Status: Inactive")

    def update_trigger_key(new_key, trigger_bot):
        if new_key and isinstance(new_key, str) and len(new_key) == 1:
            trigger_bot.set_trigger_key(new_key)
            set_status_text(status_label, f"Trigger key updated to: {new_key}")
        else:
            set_status_text(status_label, "Invalid key provided")

    
    def toggle_aimbot():
        aim_bot.toggle()
        if aim_bot.active:
            dpg.set_value(status_label, "Aimbot: Active")
            threading.Thread(target=aim_bot.run, daemon=True).start()
        else:
            dpg.set_value(status_label, "Aimbot: Inactive")

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

    status_label = create_gui(toggle_trigger, update_trigger_key, toggle_esp, toggle_defuse, update_esp_config, toggle_aimbot, toggle_bhop, trigger_bot)

    dpg.start_dearpygui()

if __name__ == '__main__':
    main()
