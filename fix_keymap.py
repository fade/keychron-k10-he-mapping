import json
import hashlib
from collections import OrderedDict

# Load original to get values
with open("Downloads/Keymap-K10 HE-11-9-34.json", "r") as f:
    orig = json.load(f)

# Modify the key in the original data structure
# Layer 2, Row 5, Col 1 -> 271 (Hyper)
l2 = orig["keymap"][2]
for k in l2:
    if k["row"] == 5 and k["col"] == 1:
        k["val"] = 271
        break

# Calculate new MD5 based ONLY on the "keymap" array
# Use separators=(',', ':') for compact formatting
keymap_json = json.dumps(orig["keymap"], separators=(",", ":"))
new_md5 = hashlib.md5(keymap_json.encode("utf-8")).hexdigest()

# Construct the output dictionary in the EXACT same order as the original
# {"id":..., "keymap":..., "version":..., "MD5":...}
out_data = OrderedDict()
out_data["id"] = orig["id"]
out_data["keymap"] = orig["keymap"]
out_data["version"] = orig["version"]
out_data["MD5"] = new_md5

# Save the whole file in compact format
with open("Downloads/Modified-Keymap-K10-HE-FINAL.json", "w") as f:
    json.dump(out_data, f, separators=(",", ":"))

print(f"File created: Downloads/Modified-Keymap-K10-HE-FINAL.json")
print(f"New MD5: {new_md5}")
