#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
#
# Used to generate mapfile.csv to append on
# linux/tools/perf/pmu-events/arch/arm64/mapfile.csv

# part number for Apple Silicon collected from Internet
apple_part_num = {
    'a14': [
        0x20, # Icestorm-A14
        0x21, # Firestorm-A14
        0x22, # Icestorm-M1
        0x23, # Firestorm-M1
        0x24, # Icestorm-M1-Pro
        0x25, # Firestorm-M1-Pro
        0x28, # Icestorm-M1-Max
        0x29, # Firestorm-M1-Max
    ],
    'a15': [
        0x30, # Blizzard-A15
        0x31, # Avalanche-A15
        0x32, # Blizzard-M2
        0x33, # Avalanche-M2
        0x34, # Blizzard-M2-Pro
        0x35, # Avalanche-M2-Pro
        0x38, # Blizzard-M2-Max
        0x39, # Avalanche-M2-Max
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

def gen_mapfile_csvlines():
    res = []
    for key in apple_part_num:
        for part_num in apple_part_num[key]:
            res.append("{:#018x},v1,apple/{},core". \
                       format(gen_apple_midr(part_num), key))
    return res

if __name__ == "__main__":
    for line in gen_mapfile_csvlines():
        print(line)
