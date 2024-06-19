#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
# Generate patch file to patch linux perf

from mapfile import apple_part_num, gen_csv_patch
from core_imp_def import gen_core_json_patch, gen_core_imp_def_dict
from argparse import ArgumentParser
import plistlib

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate patch file to patch linux perf")
    parser.add_argument("-k", "--kpep-path", help="Directory of kpep", \
                        default="/usr/share/kpep")
    parser.add_argument("-a", "--apple-pdf", \
                        help="PDF File Path for Apple-Silicon-CPU-Optimization-Guide.pdf", \
                        default=None)
    parser.add_argument("-w", "--white-list", nargs='+', help="White list of Apple part number", \
                        default=[])
    parser.add_argument("-p", "--prefix", help="Prefix perf path", default="tools/perf/")
    args = parser.parse_args()
    desc_db = dict()
    if args.apple_pdf:
        from apple_pdf_extract import extract_event_desc
        desc_db = extract_event_desc(args.apple_pdf)
    print(gen_csv_patch(args.white_list))
    for key in apple_part_num:
        if args.white_list and key not in args.white_list:
            continue
        with open(f"{args.kpep_path}/{key}.plist", 'rb') as f:
            pl = plistlib.load(f)
            filename = f"{args.prefix}pmu-events/arch/arm64/apple/{key}/core-imp-def.json"
            print(gen_core_json_patch(filename, pl, desc_db))
