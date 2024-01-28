import pyMeow as pm
from src.offsetDumper import Offsets
from src.Utils import *
from src.espBot import *
import keyboard
from pynput.mouse import Controller
import time
import math
import ctypes
from ctypes import wintypes
MOUSEEVENTF_MOVE = 0x0001
def move_mouse(x, y):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, int(x), int(y), 0, 0)
        print("coucou")
class AimBot:
    def __init__(self):
        self.active = False
        self.aim_key = "k"
        self.proc = pm.open_process("cs2.exe")
        self.mod = pm.get_module(self.proc, "client.dll")["base"]
        self.mouse = Controller()
        self.screen_width = pm.get_screen_width()
        self.screen_height = pm.get_screen_height()
        self.local_team = None
        self.is_running = False
        self.esp_bot = CS2Esp()

    def toggle(self):
        self.active = not self.active

    def set_aim_key(self, new_key):
        self.aim_key = new_key

    def run(self):
        while True:
            if self.active and keyboard.is_pressed(self.aim_key) and not self.is_running:
                self.is_running = True
                self.aim_at_enemy()
                self.is_running = False
            time.sleep(0.01)
    
    def get_closest_enemy(self):
        try:
            self.esp_bot.localTeam = pm.r_int(self.proc, pm.r_int64(self.proc, self.mod + Offsets.dwLocalPlayerController) + Offsets.m_iTeamNum)
            view_matrix = pm.r_floats(self.proc, self.mod + Offsets.dwViewMatrix, 16)
            closest_enemy = None
            closest_distance = float('inf')

            for entity in self.esp_bot.it_entities():
                if entity.team != self.esp_bot.localTeam and entity.health > 0:
                    head_pos_3D = entity.bone_pos(8)
                    screen_pos = pm.world_to_screen(view_matrix, head_pos_3D, 1)
                    if screen_pos:
                        distance = self.distance_to_center(screen_pos["x"], screen_pos["y"])
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_enemy = screen_pos
        except:
            pass
            return closest_enemy["x"], closest_enemy["y"] if closest_enemy else (None, None)

    def distance_to_center(self, x, y):
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        return math.hypot(x - center_x, y - center_y)

    def aim_at_enemy(self):
        enemy_x, enemy_y = self.get_closest_enemy()
        if enemy_x is not None and enemy_y is not None:
            delta_x = enemy_x - self.screen_width / 2
            delta_y = enemy_y - self.screen_height / 2
            move_mouse(delta_x, delta_y)
