import pyMeow as pm
import math
import time
from src.offsetDumper import Offsets

class AimBot:
    def __init__(self):
        self.proc = pm.open_process("cs2.exe")
        self.client = pm.get_module(self.proc, "client.dll")['base']
        self.engine = pm.get_module(self.proc, "engine.dll")['base']
        self.local_player = None
        self.client_state = None

    def get_local_player(self):
        return pm.r_int64(self.proc, self.client + Offsets.dwLocalPlayer)

    def get_client_state(self):
        return pm.r_int64(self.proc, self.engine + Offsets.dwClientState)

    def get_view_angles(self):
        return pm.r_vec3(self.proc, self.client_state + Offsets.dwClientState_ViewAngles)

    def set_view_angles(self, angles):
        pm.w_vec3(self.proc, self.client_state + Offsets.dwClientState_ViewAngles, angles)

    def aim_at_target(self, target_pos, local_eye_pos, current_angles):
        delta = target_pos - local_eye_pos
        hyp = math.sqrt(delta.x * delta.x + delta.y * delta.y)
        pitch = math.atan(delta.z / hyp) * 180 / math.pi
        yaw = math.atan(delta.y / delta.x) * 180 / math.pi
        if delta.x >= 0.0:
            yaw += 180.0
        return pm.vec3(pitch - current_angles.x, yaw - current_angles.y, 0)

    def main_loop(self):
        while True:
            time.sleep(0.01)
            self.local_player = self.get_local_player()
            self.client_state = self.get_client_state()

            if not pm.is_key_down(pm.VK_RBUTTON):
                continue

            local_team = pm.r_int(self.proc, self.local_player + Offsets.m_iTeamNum)
            local_eye_pos = pm.r_vec3(self.proc, self.local_player + Offsets.m_vecOrigin) + pm.r_vec3(self.proc, self.local_player + Offsets.m_vecViewOffset)
            view_angles = self.get_view_angles()

            best_fov = 5.0
            best_angle = None

            for i in range(1, 32):
                entity = pm.r_int64(self.proc, self.client + Offsets.dwEntityList + i * 0x10)
                if entity == 0:
                    continue

                if pm.r_int(self.proc, entity + Offsets.m_iTeamNum) == local_team:
                    continue

                entity_bone_matrix = pm.r_int64(self.proc, entity + Offsets.m_dwBoneMatrix)
                entity_head_pos = pm.r_vec3(self.proc, entity_bone_matrix + 0x30 * 8 + 0x0C)

                angle = self.aim_at_target(entity_head_pos, local_eye_pos, view_angles)
                fov = math.sqrt(angle.x * angle.x + angle.y * angle.y)

                if fov < best_fov:
                    best_fov = fov
                    best_angle = angle

            if best_angle:
                self.set_view_angles(view_angles + best_angle / 3.0)