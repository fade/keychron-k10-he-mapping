import json
from collections import OrderedDict
import hashlib

def calculate_md5(data):
    if "MD5" in data:
        del data["MD5"]
    content = json.dumps(data, separators=(",", ":")).encode("utf-8")
    return hashlib.md5(content).hexdigest()

# VIA Modifiers
LSFT = 512

# Target keys (Row, Col) on Layer 2/3
KEY_9 = (1, 9)
KEY_0 = (1, 10)
KEY_LBRC = (2, 11)
KEY_RBRC = (2, 12)

# Shift keys (Row, Col)
L_SHIFT = (4, 0)
R_SHIFT = (4, 12)

# MO(3) = 21024 + 3
MO_3 = 21027

# Basic QMK keycodes that should be shifted on Layer 3
# 4-29: A-Z
# 30-39: 1-0
# 40: Enter
# 44: Space
# 45-56: Punctuation (-, =, [, ], \, ;, ', `, ,, ., /)
SHIFT_RANGE = list(range(4, 40)) + list(range(45, 57))

with open("system_scripts/keychron/modified.json", "r") as f:
    data = json.load(f)

l2 = data["keymap"][2]
l3 = data["keymap"][3]

# 1. Update Layer 2
for k in l2:
    pos = (k["row"], k["col"])
    if pos == L_SHIFT or pos == R_SHIFT:
        k["val"] = MO_3
    elif pos == KEY_LBRC:
        k["val"] = LSFT + 38 # ( (LSFT + 9)
    elif pos == KEY_RBRC:
        k["val"] = LSFT + 39 # ) (LSFT + 0)

# 2. Update Layer 3 (Shift Layer)
# We rebuild Layer 3 from Layer 2
new_l3 = []
for k2 in l2:
    k3 = k2.copy()
    pos = (k3["row"], k3["col"])
    val = k3["val"]
    
    if pos == KEY_9:
        k3["val"] = 47 # [ (KC_LBRC)
    elif pos == KEY_0:
        k3["val"] = 48 # ] (KC_RBRC)
    elif pos == KEY_LBRC:
        k3["val"] = LSFT + 47 # { (LSFT + [)
    elif pos == KEY_RBRC:
        k3["val"] = LSFT + 48 # } (LSFT + ])
    elif val in SHIFT_RANGE:
        k3["val"] = LSFT + val
    # Modifiers and other keys stay as is
    new_l3.append(k3)

data["keymap"][3] = new_l3

# Re-calculate MD5 on the keymap array only
keymap_json = json.dumps(data["keymap"], separators=(",", ":"))
data["MD5"] = hashlib.md5(keymap_json.encode("utf-8")).hexdigest()

# Ensure order
out_data = OrderedDict()
out_data["id"] = data["id"]
out_data["keymap"] = data["keymap"]
out_data["version"] = data["version"]
out_data["MD5"] = data["MD5"]

with open("system_scripts/keychron/modified_swapped.json", "w") as f:
    json.dump(out_data, f, separators=(",", ":"))

print("Modified swapped keymap created.")
