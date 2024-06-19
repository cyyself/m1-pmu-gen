#!/usr/bin/env python3

import plistlib

from apple_pdf_extract import extract_event_desc

def get_brief_desc(desc):
    return desc.split("(")[0].split("Note:")[0].split(".")[0] \
               .split(",")[0].strip()

def gen_core_imp_def_dict(pl, desc = dict()):
    events = pl["system"]["cpu"]["events"]
    res = []
    for key, value in events.items():
        if value.get('number') is not None:
            # Use key itself if the desc not found
            PublicDescription = desc.get(key, key)
            BriefDescription = get_brief_desc(PublicDescription)
            res.append({
                "PublicDescription": PublicDescription,
                "EventCode": str(hex(value['number'])),
                "EventName": key,
                "BriefDescription": BriefDescription,
            })
    return res
            
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <plist_filename> [apple_pdf=None]")
        print(f"Example: {sys.argv[0]} /usr/share/kpep/a14.plist",
               "Apple-Silicon-CPU-Optimization-Guide.pdf")
        sys.exit(1)
    filename = sys.argv[1]
    apple_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    pl = dict()
    with open(filename, 'rb') as f:
        pl = plistlib.load(f)
    desc_db = dict()
    if apple_pdf:
        desc_db = extract_event_desc(apple_pdf)
    res = gen_core_imp_def_dict(pl, desc_db)
    import json
    json.dump(res, sys.stdout, indent=4)