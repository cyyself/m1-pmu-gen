#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
# 
# Used to Extract PMU event description from Apple Silicon CPU Optimization
# Guide which can be downloaded from
# https://developer.apple.com/download/apple-silicon-cpu-optimization-guide/

def extract_event_desc(pdf_path):
    import pymupdf
    import re
    import tqdm
    import sys
    def is_event_name(s):
        s = s.strip()
        return re.match(r"^[A-Z][A-Z0-9_]+$", s)
    doc = pymupdf.open(pdf_path)
    result = dict()
    for page in tqdm.tqdm(doc.pages(), total=doc.page_count):
        text = page.get_text()
        if "Event Name" not in text or \
           "Brief Description" not in text:
            continue
        tabs = page.find_tables()
        if tabs.tables:
            for tab in tabs.tables:
                cur_table = tab.extract()
                try:
                    header = cur_table[0]
                    if header[0].strip() == 'Event Name' and \
                       header[1].strip() == 'Brief Description':
                        # Here we start to extract event description
                        for row in cur_table[1:]:
                            event = ""
                            desc = ""
                            try:
                                event = row[0].strip()
                                desc = row[1].strip()
                            except:
                                continue
                            if "\n" in event:
                                event = event.split("\n")[0].strip()
                            if not is_event_name(event):
                                continue
                            result[event] = " ".join([x.strip() for x in desc.split("\n")])
                except:
                    print("Failed to extract table on page:", page.number, file=sys.stderr)
                    exit(1)
    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: ./apple_pdf_extract.py <pdf_path to Apple-Silicon-CPU-Optimization-Guide.pdf>")
        sys.exit(1)
    file = sys.argv[1]
    res = extract_event_desc(file)
    for key, value in res.items():
        print(f"{key}: {value}")
