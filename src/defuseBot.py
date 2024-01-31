import time
from src.offsetDumper import Offsets
import pyMeow as pm
from src.Utils import *

class DefuseBot:
    def __init__(self):
        self.active = False
        self.proc = pm.open_process("cs2.exe")
        self.mod = pm.get_module(self.proc, "client.dll")["base"]
        self.player = pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerPawn)
        self.defuse_start_time = None
        self.defusing_with_kit = False 
    
    def toggle(self):
        self.active = not self.active

    def run(self):
        pm.overlay_init("Counter-Strike 2", fps=144)
        while pm.overlay_loop():
            pm.begin_drawing()
            pm.draw_fps(0, 0)
            planted = pm.r_bool(self.proc, self.mod + Offsets.dwPlantedC4 - 0x8)
            for i in range(16):
                entity = pm.r_int64(self.proc, self.mod + Offsets.dwEntityList)
                list_entity = pm.r_int64(self.proc, entity + ((8 * (i & 0x7FFF) >> 9) + 16))
                if list_entity == 0:
                    continue
                entity_controller = pm.r_int64(self.proc, list_entity + 120 * (i & 0x1FF))
                if entity_controller == 0:
                    continue
                entity_controller_pawn = pm.r_int64(self.proc, entity_controller + Offsets.m_hPlayerPawn)
                if entity_controller_pawn == 0:
                    continue
                list_entity = pm.r_int64(self.proc, entity + (0x8 * ((entity_controller_pawn & 0x7FFF) >> 9) + 16))
                if list_entity == 0:
                    continue
                entity_pawn = pm.r_int64(self.proc, list_entity + (120) * (entity_controller_pawn & 0x1FF))
                if entity_pawn == 0:
                    continue
                isDefusing = pm.r_bool(self.proc, entity_pawn + Offsets.m_bIsDefusing)
                hasKit = pm.r_bool(self.proc, entity_pawn + Offsets.m_bHasDefuser)
                player_team = pm.r_int(self.proc, entity_pawn + Offsets.m_iTeamNum)
                my_team = pm.r_int(self.proc, self.player + Offsets.m_iTeamNum)
                if planted and (player_team != my_team) and isDefusing:
                    if self.defuse_start_time is None:
                        self.defuse_start_time = time.time()
                        self.defusing_with_kit = hasKit
                    time_passed = time.time() - self.defuse_start_time
                    time_left = (5 if self.defusing_with_kit else 10) - time_passed
                    defuse_text = "Defusing with Kit" if self.defusing_with_kit else "Defusing without Kit"
                    pm.draw_text(defuse_text, 50, 50, 20, Colors.white)
                    pm.draw_text(f"Time left: {max(0, round(time_left, 1))}s", 50, 70, 20, Colors.white)
            if self.defuse_start_time and not isDefusing:
                self.defuse_start_time = None
            pm.end_drawing()
            time.sleep(0.01)