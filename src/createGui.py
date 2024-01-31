import dearpygui.dearpygui as dpg
import sys

def on_close():
    dpg.stop_dearpygui()
    sys.exit(0)

def create_gui(toggle_trigger, update_trigger_key, toggle_esp, toggle_noflash, update_esp_config, toggle_aimbot, toggle_bhop, trigger_bot, toggle_all):
    dpg.create_context()
    window_width, window_height = 400, 300
    with dpg.window(label="Cs2 Cheat", width=window_width, height=window_height, no_move=True, no_resize=True, no_title_bar=False, no_scrollbar=True, no_collapse=True):
        with dpg.tab_bar():
            with dpg.tab(label="General"):
                dpg.add_button(label="Toggle All Features", callback=toggle_all)
            # Onglet Aim
            with dpg.tab(label="Trigger"):
                dpg.add_button(label="Toggle Trigger Bot", callback=toggle_trigger)
                trigger_key_input = dpg.add_input_text(label="Trigger Key", default_value="x", tag="trigger_key_input")
                dpg.add_button(label="Update Key", callback=lambda: update_trigger_key(dpg.get_value("trigger_key_input"), trigger_bot))

            # Onglet ESP
            with dpg.tab(label="ESP"):
                dpg.add_button(label="Toggle ESP", callback=toggle_esp)
                dpg.add_checkbox(label="Show Box", default_value=True, callback=lambda s,d: update_esp_config("box", dpg.get_value(s)))
                dpg.add_checkbox(label="Show Health", default_value=True, callback=lambda s,d: update_esp_config("health", dpg.get_value(s)))
                dpg.add_checkbox(label="Show Name", default_value=True, callback=lambda s,d: update_esp_config("name", dpg.get_value(s)))
                dpg.add_checkbox(label="Show Skeleton", default_value=True, callback=lambda s,d: update_esp_config("skeleton", dpg.get_value(s)))
                dpg.add_checkbox(label="Show Head", default_value=True, callback=lambda s,d: update_esp_config("Head", dpg.get_value(s)))

            # Onglet Aim
            with dpg.tab(label="Aim Bot"):
                dpg.add_button(label="Toggle AimBot", callback=toggle_aimbot)

            # Onglet Misc
            with dpg.tab(label="Misc"):
                dpg.add_button(label="Toggle Auto Bhop", callback=toggle_bhop)
                dpg.add_button(label="Toggle No Flash", callback=toggle_noflash)

        status_label = dpg.add_text("Status: Inactive")

    dpg.create_viewport(title='Cs2 Cheat', width=window_width, height=window_height, decorated=False)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    return status_label

def set_status_text(label, text):
    dpg.set_value(label, text)
