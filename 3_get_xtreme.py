#!/usr/bin/env python
# coding: utf-8

import json
import os
from shutil import copyfile

urls = json.load(open('url.json'))

os.makedirs('data/xtreme/dev', exist_ok=True)
os.makedirs('data/xtreme/test', exist_ok=True)

for id in urls['xtreme_dev_ids']:
    source = f"data/clean/dev/{id}.json"
    target = f"data/xtreme/dev/{id}.json"
    try:
        copyfile(source, target)
    except:
        continue
for id in urls['xtreme_test_ids']:
    source = f"data/clean/test/{id}.json"
    target = f"data/xtreme/test/{id}.json"
    try:
        copyfile(source, target)
    except:
        continue

