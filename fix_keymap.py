"""Set the keycode on the K10 HE's left Win key and rewrite the checksum.

Usage: python3 fix_keymap.py KEYMAP.json KEYCODE [OUT.json]

Sets row 5, column 1 on layers 2 and 3 (the Win/Linux base layer and its
Fn layer) to KEYCODE and writes the file back, or to OUT.json when given.
The Launcher refuses a file whose MD5 does not match its keymap, so the
checksum is recomputed over the compact JSON of the keymap array, and the
top-level keys keep the order the Launcher exported them in.
"""

import hashlib
import json
import sys

ROW, COL = 5, 1
LAYERS = (2, 3)


def main(argv):
    if len(argv) not in (3, 4):
        sys.exit(__doc__.strip().splitlines()[2])
    src, keycode = argv[1], int(argv[2], 0)
    dst = argv[3] if len(argv) == 4 else src

    with open(src) as f:
        data = json.load(f)

    for layer in LAYERS:
        hits = [k for k in data["keymap"][layer] if (k["row"], k["col"]) == (ROW, COL)]
        if len(hits) != 1:
            sys.exit(f"layer {layer}: expected one key at row {ROW} col {COL}, found {len(hits)}")
        hits[0]["val"] = keycode

    keymap = json.dumps(data["keymap"], separators=(",", ":"))
    out = {
        "id": data["id"],
        "keymap": data["keymap"],
        "version": data["version"],
        "MD5": hashlib.md5(keymap.encode("utf-8")).hexdigest(),
    }
    with open(dst, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"{dst}: row {ROW} col {COL} = {keycode} on layers {LAYERS}, MD5 {out['MD5']}")


if __name__ == "__main__":
    main(sys.argv)
