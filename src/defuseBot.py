import time
from src.offsetDumper import Offsets
import pyMeow as pm

class DefuseBot:
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
            ent_list = pm.r_int64(self.proc, self.mod + Offsets.dwEntityList)
            for i in range(1, 65):
                bomb_ptr = pm.r_int64(self.proc, ent_list + i * 0x10)
                if bomb_ptr == 0:
                    continue
                planted = pm.r_bool(self.proc, bomb_ptr + Offsets.m_bC4Activated)
                bomb_defused = pm.r_bool(self.proc, bomb_ptr + Offsets.m_bBombDefused)
                bomb_exploded = pm.r_bool(self.proc, bomb_ptr + Offsets.m_bHasExploded)
                
                if planted and not bomb_defused and not bomb_exploded:
                    being_defused = pm.r_bool(self.proc, bomb_ptr + Offsets.m_bBeingDefused)
                    bomb_site = pm.r_int(self.proc, bomb_ptr + Offsets.m_nBombSite)
                    site = "B" if bomb_site > 0 else "A"
                    defusing_message = "Defusing: " if being_defused else "Waiting for defuse: "
                    print(f"Bomb planted on: {site}\n{defusing_message}")
                elif bomb_defused:
                    print("Bomb Defused!")
                    break
                elif bomb_exploded:
                    print("Bomb Exploded!")
                    break

            time.sleep(1)
