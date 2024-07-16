import pyMeow as pm
from src.offsetDumper import Offsets
from src.Utils import *


class CS2Esp:
    def __init__(self):
        self.active = False
        self.proc = pm.open_process("cs2.exe")
        self.mod = pm.get_module(self.proc, "client.dll")["base"]
        self.show_box = True
        self.show_health = True
        self.show_name = True
        self.show_weapon = True
        self.show_skeleton = True
        self.show_head = True
        self.localTeam = None

    def toggle(self):
        self.active = not self.active

    def update_config(self, show_box=True, show_health=True, show_name=True, show_weapon=True):
        self.show_box = show_box
        self.show_health = show_health
        self.show_name = show_name
        self.show_weapon = show_weapon

    def it_entities(self):
        entList = pm.r_int64(self.proc, self.mod + Offsets.dwEntityList)
        local = pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerController)
        
        for i in range(1, 65):
            try:
                entryPtr = pm.r_int64(self.proc, entList + (8 * (i & 0x7FFF) >> 9) + 16)
                controllerPtr = pm.r_int64(self.proc, entryPtr + 120 * (i & 0x1FF))
                if controllerPtr == local:
                    self.localTeam = pm.r_int(self.proc, local + Offsets.m_iTeamNum)
                    continue
                controllerPawnPtr = pm.r_int64(self.proc, controllerPtr + Offsets.m_hPlayerPawn)
                listEntryPtr = pm.r_int64(self.proc, entList + 0x8 * ((controllerPawnPtr & 0x7FFF) >> 9) + 16)
                pawnPtr = pm.r_int64(self.proc, listEntryPtr + 120 * (controllerPawnPtr & 0x1FF))
            except:
                continue
            yield Entity(controllerPtr, pawnPtr, self.proc)

    def draw_skeleton(self, ent, viewMatrix):
        try:
            cou = pm.world_to_screen(viewMatrix, ent.bone_pos(5), 1)
            shoulderR = pm.world_to_screen(viewMatrix, ent.bone_pos(8), 1)
            shoulderL = pm.world_to_screen(viewMatrix, ent.bone_pos(13), 1)
            brasR = pm.world_to_screen(viewMatrix, ent.bone_pos(9), 1)
            brasL = pm.world_to_screen(viewMatrix, ent.bone_pos(14), 1)
            handR = pm.world_to_screen(viewMatrix, ent.bone_pos(11), 1)
            handL = pm.world_to_screen(viewMatrix, ent.bone_pos(16), 1)
            waist = pm.world_to_screen(viewMatrix, ent.bone_pos(0), 1)
            kneesR = pm.world_to_screen(viewMatrix, ent.bone_pos(23), 1)
            kneesL = pm.world_to_screen(viewMatrix, ent.bone_pos(26), 1)
            feetR = pm.world_to_screen(viewMatrix, ent.bone_pos(24), 1)
            feetL = pm.world_to_screen(viewMatrix, ent.bone_pos(27), 1)

            pm.draw_line(cou["x"], cou["y"], shoulderR["x"], shoulderR["y"], Colors.white, 1)
            pm.draw_line(cou["x"], cou["y"], shoulderL["x"], shoulderL["y"], Colors.white, 1)
            pm.draw_line(brasL["x"], brasL["y"], shoulderL["x"], shoulderL["y"], Colors.white, 1)
            pm.draw_line(brasR["x"], brasR["y"], shoulderR["x"], shoulderR["y"], Colors.white, 1)
            pm.draw_line(brasR["x"], brasR["y"], handR["x"], handR["y"], Colors.white, 1)
            pm.draw_line(brasL["x"], brasL["y"], handL["x"], handL["y"], Colors.white, 1)
            pm.draw_line(cou["x"], cou["y"], waist["x"], waist["y"], Colors.white, 1)
            pm.draw_line(kneesR["x"], kneesR["y"], waist["x"], waist["y"], Colors.white, 1)
            pm.draw_line(kneesL["x"], kneesL["y"], waist["x"], waist["y"], Colors.white, 1)
            pm.draw_line(kneesL["x"], kneesL["y"], feetL["x"], feetL["y"], Colors.white, 1)
            pm.draw_line(kneesR["x"], kneesR["y"], feetR["x"], feetR["y"], Colors.white, 1)
        except:
            pass

    def run(self):
        pm.overlay_init("Counter-Strike 2", fps=144)
        while pm.overlay_loop():
            pm.begin_drawing()
            pm.draw_fps(0, 0)
            view_matrix = pm.r_floats(self.proc, self.mod + Offsets.dwViewMatrix, 16)

            if self.localTeam is None:
                local = pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerController)
                self.localTeam = pm.r_int(self.proc, local + Offsets.m_iTeamNum)

            for ent in self.it_entities():
                if ent.wts(view_matrix) and ent.health > 0 and ent.team != self.localTeam:
                    color = Colors.cyan if ent.team != 2 else Colors.orange
                    head = ent.pos2d["y"] - ent.head_pos2d["y"]
                    width = head / 2
                    center = width / 2
                    
                    if self.show_box:
                        pm.draw_rectangle_lines(
                            ent.head_pos2d["x"] - center,
                            ent.head_pos2d["y"] - center / 2,
                            width,
                            head + center / 2,
                            color,
                            1.2,
                        )
                    if self.show_health:
                        pm.draw_rectangle_rounded(
                            ent.head_pos2d["x"] - center - 10,
                            ent.head_pos2d["y"] + (head * (100 - ent.health) / 100),
                            3,
                            head - (head * (100 - ent.health) / 100),
                            0,
                            1,
                            Colors.green,
                        )
                    if self.show_name:
                        pm.draw_text(
                            ent.name,
                            ent.head_pos2d["x"] - pm.measure_text(ent.name, 7) // 2,
                            ent.head_pos2d["y"] - center / 2,
                            7,
                            Colors.white,
                        )
                    if self.show_head:
                        pm.draw_circle_sector(
                            ent.head_pos2d["x"],
                            ent.head_pos2d["y"],
                            center / 3,
                            0,
                            360,
                            0,
                            Colors.red,
                        )
                    if self.show_skeleton:
                        self.draw_skeleton(ent, view_matrix)
            pm.end_drawing()
