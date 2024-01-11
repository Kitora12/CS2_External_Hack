import time
from src.offsetDumper import Offsets
import pyMeow as pm

class DefuseBot:
    def __init__(self):
        self.active = False
        self.proc = pm.open_process("cs2.exe")
        self.mod = pm.get_module(self.proc, "client.dll")["base"]
        self.planted = False
        self.plant_time = 0
    
    def toggle(self):
        self.active = not self.active

    def is_bomb_planted(self):
        planted_address = self.mod + Offsets.dwPlantedC4 - 0x8
        is_planted = pm.r_bool(self.proc, planted_address)
        return is_planted

    def get_bomb_site(self):
        c_planted_c4_ptr = pm.r_int64(self.proc, self.mod + Offsets.dwPlantedC4)
        if c_planted_c4_ptr != 0:
            offset_address = c_planted_c4_ptr + Offsets.m_bBeingDefused
            print(f"Address to read: {offset_address}")
            pm.r_bool(self.proc, offset_address)
        return None

    def run(self):
        while True:
            is_bomb_planted = self.is_bomb_planted()
            current_time = time.time() * 1000

            if is_bomb_planted and (not self.planted or current_time - self.plant_time > 60000):
                self.planted = True
                self.plant_time = current_time

            remaining = (40000 - (current_time - self.plant_time)) / 1000

            if self.planted:
                print(f"Bomb on planted: {remaining:.3f} s")
            else:
                print("C4 not planted")
            
            time.sleep(1)