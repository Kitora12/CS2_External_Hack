from src.offsetDumper import Offsets
import pyMeow as pm
from src.Utils import *

class NoFlash:
    def __init__(self):
        self.active = False
        self.proc = pm.open_process("cs2.exe")
        self.mod = pm.get_module(self.proc, "client.dll")["base"]
    
    def toggle(self):
        self.active = not self.active

    def run(self):
        try:
            (flashAddress,) = pm.aob_scan_module(self.proc, pm.get_module(self.proc, "client.dll")["name"], "0f 83 ?? ?? ?? ?? 48 8b 1d ?? ?? ?? ?? 40 38 73")
        except:
            (flashAddress,) = pm.aob_scan_module(self.proc, pm.get_module(self.proc, "client.dll")["name"], "0f 82 ?? ?? ?? ?? 48 8b 1d ?? ?? ?? ?? 40 38 73")
        
        if self.active:
            pm.w_bytes(self.proc, flashAddress, b"\x0f\x82")
        else:
            pm.w_bytes(self.proc, flashAddress, b"\x0f\x83")