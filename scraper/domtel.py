#!/usr/bin/python3
from utils import get_team_member, gender_icon, get_award, get_cat_award
from urllib.request import Request, urlopen
import json
import re
import sys

def get_domtel_results(url):
    req = Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )

    with urlopen(req) as response:
        return response.read().decode('utf-8')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python domtel.py <domtel_url>")
        sys.exit(1)

    target_url = sys.argv[1]
    html_data = get_domtel_results(target_url)

    match = re.search(r"<title>(.*)&", html_data)
    print(f"[] {match.group(1)}")

    match = re.search(r"var\s+ptc_vars\s*=(.*);", html_data)
    data = json.loads(match.group(1).strip(';'))['init_data']

    for r in data:
        if not r['Msc']:
            continue
        name = r['Zawodnik']
        member = get_team_member(name)
        if not member:
            continue
        pos = r['Msc']
        gender = r['Płeć']
        time = r['Czas netto']
        pos_open = int(r['Msc'])
        pos_cat = int(r['M/Kat'])
        total = len([e for e in data if e['DYSTANS'] == r['DYSTANS'] and e['Msc']])
        print(f"{member} {gender_icon(gender[0])} {pos}/{total} ⏱️{time} {get_award(pos_open)} {get_cat_award(pos_cat)}")

    print(f"🔗 {target_url}")
