import time
import win32api
from src.offsetDumper import Offsets
import pyMeow as pm

class bhopBot:
    def __init__(self):
        self.active = False
        self.proc = pm.open_process("cs2.exe")
        self.mod = pm.get_module(self.proc, "client.dll")["base"]

    def toggle(self):
        self.active = not self.active

    def run(self):
        while True:
            if not self.active:
                time.sleep(0.1)
                continue

            if win32api.GetAsyncKeyState(0x20):
                player = pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerPawn)
                if player:
                    flag = pm.r_int(self.proc, player + Offsets.m_fFlags)
                    if flag & (1 << 0): 
                        time.sleep(0.015625)
                        pm.w_int(self.proc, self.mod + Offsets.dwForceJump, 65537)
                        time.sleep(0.02)
                        pm.w_int(self.proc, self.mod + Offsets.dwForceJump, 256)
            time.sleep(0.01)
