import pyMeow as pm
from src.offsetDumper import Offsets

class Entity:
    def __init__(self, ptr, pawn_ptr, proc, weapon_name):
        self.ptr = ptr
        self.pawn_ptr = pawn_ptr
        self.proc = proc
        self.pos2d = None
        self.head_pos2d = None
        self.weapon_name = weapon_name
        

    @property
    def name(self):
        return pm.r_string(self.proc, self.ptr + Offsets.m_iszPlayerName)

    @property
    def health(self):
        return pm.r_int(self.proc, self.pawn_ptr + Offsets.m_iHealth)

    @property
    def team(self):
        return pm.r_int(self.proc, self.pawn_ptr + Offsets.m_iTeamNum)

    @property
    def pos(self):
        return pm.r_vec3(self.proc, self.pawn_ptr + Offsets.m_vOldOrigin)

    def bone_pos(self, bone):
        game_scene = pm.r_int64(self.proc, self.pawn_ptr + Offsets.m_pGameSceneNode)
        bone_array_ptr = pm.r_int64(self.proc, game_scene + Offsets.m_pBoneArray)
        return pm.r_vec3(self.proc, bone_array_ptr + bone * 32)


    def wts(self, view_matrix):
        try:
            self.pos2d = pm.world_to_screen(view_matrix, self.pos, 1)
            self.head_pos2d = pm.world_to_screen(view_matrix, self.bone_pos(6), 1)
        except:
            return False
        return True
    
    def get_weapon_name(self, player_pawn_ptr):
            C_CSWeaponBase = pm.r_int64(self.proc, player_pawn_ptr + Offsets.m_pClippingWeapon)
            weaponData = pm.r_int64(self.proc, C_CSWeaponBase + Offsets.m_nSubclassID + 0x8)
            weaponNameAddress = pm.r_int64(self.proc, weaponData + Offsets.m_szName)

            if not weaponNameAddress:
                return "NULL"
            else:
                weaponName = pm.r_string(self.proc, weaponNameAddress, 260)
                return weaponName[7:] if weaponName.startswith("weapon_") else weaponName
class Colors:
    orange = pm.get_color("orange")
    black = pm.get_color("black")
    cyan = pm.get_color("cyan")
    white = pm.get_color("white")
    grey = pm.fade_color(pm.get_color("#242625"), 0.7)
    green = pm.get_color("green")
    red = pm.get_color("red")
