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

    def get_weapon_name(self, player_pawn_ptr):
            C_CSWeaponBase = pm.r_int64(self.proc, player_pawn_ptr + Offsets.m_pClippingWeapon)
            weaponData = pm.r_int64(self.proc, C_CSWeaponBase + Offsets.m_nSubclassID + 0x8)
            weaponNameAddress = pm.r_int64(self.proc, weaponData + Offsets.m_szName)

            if not weaponNameAddress:
                return "NULL"
            else:
                weaponName = pm.r_string(self.proc, weaponNameAddress, 260)
                return weaponName[7:] if weaponName.startswith("weapon_") else weaponName

    def update_config(self, show_box=True, show_health=True, show_name=True, show_weapon=True):
        self.show_box = show_box
        self.show_health = show_health
        self.show_name = show_name
        self.show_weapon = show_weapon

    def it_entities(self):
        ent_list = pm.r_int64(self.proc, self.mod + Offsets.dwEntityList)
        local = pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerController)

        for i in range(16):
            try:
                entry_ptr = pm.r_int64(self.proc, ent_list + (8 * (i & 0x7FFF) >> 9) + 16)
                controller_ptr = pm.r_int64(self.proc, entry_ptr + 120 * (i & 0x1FF))
                if controller_ptr == local:
                    self.localTeam = pm.r_int(self.proc, local + Offsets.m_iTeamNum)
                    continue
                controller_pawn_ptr = pm.r_int64(self.proc, controller_ptr + Offsets.m_hPlayerPawn)
                listEntryPtr = pm.r_int64(self.proc, ent_list + 0x8 * ((controller_pawn_ptr & 0x7FFF) >> 9) + 16)
                pawnPtr = pm.r_int64(self.proc, listEntryPtr + 120 * (controller_pawn_ptr & 0x1FF))
                team = pm.r_int(self.proc, pawnPtr + Offsets.m_iTeamNum)
                if team != self.localTeam:
                    weapon_name = self.get_weapon_name(pawnPtr)
                    yield Entity(controller_ptr, pawnPtr, self.proc, weapon_name=weapon_name)
            except:
                continue

    def draw_skeleton(self, ent, view_matrix):
        try:
            bone_relations = [(5, 8), (5, 13), (8, 9), (13, 14), (9, 11), (14, 16), 
                            (5, 0), (0, 23), (0, 26), (23, 24), (26, 27)]
            
            for bone_start, bone_end in bone_relations:
                start_pos = ent.bone_pos(bone_start)
                end_pos = ent.bone_pos(bone_end)
                start_screen = pm.world_to_screen(view_matrix, start_pos, 1)
                end_screen = pm.world_to_screen(view_matrix, end_pos, 1)

                if not start_screen or not end_screen:
                    continue

                pm.draw_line(start_screen["x"], start_screen["y"], 
                            end_screen["x"], end_screen["y"], 
                            Colors.white, 1)
        except:
            pass

    def run(self):
        pm.overlay_init("Counter-Strike 2", fps=144)
        while pm.overlay_loop():
            pm.begin_drawing()
            pm.draw_fps(0, 0)
            view_matrix = pm.r_floats(self.proc, self.mod + Offsets.dwViewMatrix, 16)
            for ent in self.it_entities():
                if ent.wts(view_matrix) and ent.health > 0:
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
                                head + center / 2,
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
                    if self.show_weapon:
                        weapon_text = f"Weapon: {ent.weapon_name}"
                        pm.draw_text(
                            weapon_text,
                            ent.head_pos2d["x"] - pm.measure_text(weapon_text, 7) // 2,
                            ent.head_pos2d["y"] - center / 2 - 20,
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
