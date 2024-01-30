import keyboard, time
from pynput.mouse import Controller, Button
from win32gui import GetWindowText, GetForegroundWindow
from random import uniform
from src.offsetDumper import Offsets
import pyMeow as pm

class TriggerBot:
    def __init__(self):
        self.active = False
        self.trigger_key = "x"
        self.proc = pm.open_process("cs2.exe")
        self.mod = pm.get_module(self.proc, "client.dll")["base"]
        self.mouse = Controller()

    def toggle(self):
        self.active = not self.active

    def set_trigger_key(self, new_key):
        if new_key and isinstance(new_key, str) and len(new_key) > 0:
            self.trigger_key = new_key
        else:
            print("Invalid key provided for TriggerBot")


    def run(self):
        while True:
            if keyboard.is_pressed(self.trigger_key):
                player = pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerPawn)
                entityId = pm.r_int(self.proc, player + Offsets.m_iIDEntIndex)
                if entityId > 0:
                    entList = pm.r_int64(self.proc, self.mod + Offsets.dwEntityList)
                    entEntry = pm.r_int64(self.proc, entList + 0x8 * (entityId >> 9) + 0x10)
                    entity = pm.r_int64(self.proc, entEntry + 120 * (entityId & 0x1FF))
                    entityTeam = pm.r_int(self.proc, entity + Offsets.m_iTeamNum)
                    playerTeam = pm.r_int(self.proc, player + Offsets.m_iTeamNum)
                    if entityTeam != playerTeam:
                        entityHp = pm.r_int(self.proc, entity + Offsets.m_iHealth)
                        if entityHp > 0:
                            time.sleep(uniform(0.01, 0.02))
                            self.mouse.press(Button.left)
                            time.sleep(uniform(0.01, 0.04))
                            self.mouse.release(Button.left)
                time.sleep(0.02)
            else:
                time.sleep(0.1)
