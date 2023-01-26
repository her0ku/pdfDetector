import fitz
import os

import signatures

def check_metadata(metadata):
    for meta_elem in signatures.warning_list:
        if(meta_elem in metadata.lower()):
            return 'Warning, using popular pdf-exploit program ' + meta_elem
    return 'OK'


def check_exploit(bad_objects):
    alerts = []
    for elem in bad_objects:
        for js_item in signatures.js_stop_list:
            if js_item in elem.lower():
                alerts.append((elem.lower(), js_item))
    return alerts

def pdf_analyzer(src):
    bad_objects = []
    f = open(src, "r", encoding='utf-8', errors='ignore')
             
    flag = False
    doc = fitz.open(f)
    metadata = str(doc.metadata)
    bad_meta = check_metadata(metadata)
    for line in map(str.strip, f.readlines()):
        if flag:
            if ">>" in line:
                flag = False
            else:
                bad_objects.append(line)
        elif '/S /JavaScript' in line:
            flag = True

    os.remove(src)
    if bad_objects:
        exploit_result = check_exploit(bad_objects)
        if exploit_result:
            return bad_meta, str(exploit_result)
        else:
            return bad_meta, 'OK'
    else:
        return bad_meta, 'OK'

        