#!/usr/bin/env python3

import json
import datetime
import sys
import urllib.request
from urllib.error import HTTPError


def header(text, fillchar='-', width=40):
    tofill = max(width - 4 - len(text), 0)
    leftpad = tofill // 2

    print('{}[ {} ]{}'.format(
        fillchar * leftpad,
        text,
        fillchar * (tofill - leftpad),
    ))


# What day
weekdagen = ('ma', 'di', 'wo', 'do', 'vr')
deltas = {'morgen': 1,
          'overmorgen': 2}

d = datetime.date.today()
if len(sys.argv) == 2:
    d += datetime.timedelta(deltas.get(sys.argv[1], 0))

    if sys.argv[1][0:2] in weekdagen:
        while d.weekday() != weekdagen.index(sys.argv[1][0:2]):
            d += datetime.timedelta(1)

# Fetch from API
try:
    menu = json.loads(urllib.request.urlopen(
        "http://zeus.ugent.be/hydra/api/2.0/resto/menu/nl/{}/{}/{}.json".format(d.year, d.month, d.day)).read().decode(
        'utf-8'))
    # Print menu
    print(menu)

    header(str(d), fillchar='=')

    header('SOEP')
    for s in menu["meals"]:
        if s["kind"] == "soup":
            print("* {}".format(s["name"]))

    header('HOOFDGERECHTEN')
    for m in menu["meals"]:
        if m["kind"] == "meat":
            print("* Vlees: {}".format(m["name"]))
        elif m["kind"] == "fish":
            print("* Vis: {}".format(m["name"]))
        elif m["kind"] == "vegetarian":
            print("* Vegetarisch: {}".format(m["name"]))

    header('GROENTEN')
    for v in menu["vegetables"]:
        print("* {}".format(v))
except HTTPError:
    exit("Restaurant gesloten")
