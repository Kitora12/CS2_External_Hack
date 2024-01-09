import requests

class Offsets:
    m_pBoneArray = 480

class OffsetDumper:
    @staticmethod
    def fetch_and_set_offsets():
        offsets = requests.get("https://raw.githubusercontent.com/a2x/cs2-dumper/main/generated/offsets.json").json()
        client_dll = requests.get("https://raw.githubusercontent.com/a2x/cs2-dumper/9a13b18e5bddb9bc59d5cd9a3693b39fd8d6849b/generated/client.dll.json").json()

        for k in offsets["client_dll"]["data"]:
            setattr(Offsets, k, offsets["client_dll"]["data"][k]["value"])

        for k, v in client_dll.items():
            for sub_k in v["data"]:
                setattr(Offsets, sub_k, v["data"][sub_k]["value"])
