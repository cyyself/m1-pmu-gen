#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
#
# Used to generate mapfile.csv to append on
# linux/tools/perf/pmu-events/arch/arm64/mapfile.csv

# part number for Apple Silicon collected from Internet
apple_part_num = {
    'a14': [
        (0x20, 'icestorm',  'a14'),
        (0x21, 'firestorm', 'a14'),
        (0x22, 'icestorm',  'm1'),
        (0x23, 'firestorm', 'm1'),
        (0x24, 'icestorm',  'm1-pro'),
        (0x25, 'firestorm', 'm1-pro'),
        (0x28, 'icestorm',  'm1-max'),
        (0x29, 'firestorm', 'm1-max'),
    ],
    'a15': [
        (0x30, 'blizzard',  'a15'),
        (0x31, 'avalanche', 'a15'),
        (0x32, 'blizzard',  'm2'),
        (0x33, 'avalanche', 'm2'),
        (0x34, 'blizzard',  'm2-pro'),
        (0x35, 'avalanche', 'm2-pro'),
        (0x38, 'blizzard',  'm2-max'),
        (0x39, 'avalanche', 'm2-max'),
    ]
}

def gen_apple_midr(part_num):
    revision = 0x0
    partNum = part_num
    archId = 0xf
    variant = 0x0
    impId = 0x61
    return sum([revision << 0,
                partNum << 4,
                archId << 16,
                variant << 20,
                impId << 24])

def gen_mapfile_csvlines(white_list=None):
    res = []
    for key in apple_part_num:
        if white_list and key not in white_list:
            continue
        for part_num, uarch, soc in apple_part_num[key]:
            res.append("{:#018x},v1,apple/{},core". \
                       format(gen_apple_midr(part_num), key))
    return res

def gen_csv_patch(white_list=None):
    lines = list(map(lambda x: '+' + x, gen_mapfile_csvlines(white_list)))
    return f"""
diff --git a/tools/perf/pmu-events/arch/arm64/mapfile.csv b/tools/perf/pmu-events/arch/arm64/mapfile.csv
--- a/tools/perf/pmu-events/arch/arm64/mapfile.csv
+++ b/tools/perf/pmu-events/arch/arm64/mapfile.csv
@@ -45,0 +45,{len(lines)} @@
{"\n".join(lines)}
""".strip()

if __name__ == "__main__":
    for line in gen_mapfile_csvlines():
        print(line)
