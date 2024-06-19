#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
# 
# Used to Extract PMU event description from Apple Silicon CPU Optimization
# Guide which can be downloaded from
# https://developer.apple.com/download/apple-silicon-cpu-optimization-guide/

def extract_event_desc(pdf_path):
    import pymupdf
    import re
    end_sentense = ["Apple Silicon CPU Optimization Guide", "spacer"]
    def is_event_name(s):
        s = s.strip()
        return re.match(r"^[A-Z0-9_]+$", s)
    doc = pymupdf.open(pdf_path)
    result = dict()
    for page in doc:
        text = page.get_text().split("\n")
        for idx in range(len(text)-1):
            if [text[idx].strip(), text[idx+1].strip()] == \
               ["Event Name", "Brief Description"]:
                    # Here we start to extract event description
                    idx += 2
                    while idx + 1 < len(text):
                        event = text[idx].strip()
                        if not is_event_name(event):
                            break
                        idx += 1
                        desc = text[idx].strip()
                        idx += 1
                        desc_idx = idx
                        while desc_idx < len(text) and \
                              (not is_event_name(text[desc_idx])) and \
                              (not text[desc_idx].strip() in end_sentense):
                            desc += " " + text[desc_idx].strip()
                            desc_idx += 1
                        result[event] = desc
                        idx = desc_idx
                    break
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