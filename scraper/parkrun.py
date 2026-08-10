#!/usr/bin/python3
from utils import get_team_member, gender_icon, get_award
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from html.parser import HTMLParser
import re
import sys

class ParkrunParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.current_row = None
        self.current_field = None
        self.in_row = False
        self.m_pos = 0
        self.f_pos = 0

        # Title extraction
        self.in_title = False
        self.event_title = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '')

        # Track <title> tag start
        if tag == 'title' and self.event_title == '':
            self.in_title = True
            return

        # 1. Detect start of a runner's row
        if tag == 'tr' and 'Results-table-row' in classes:
            self.in_row = True
            self.current_row = {
                'position': '',
                'name': '',
                'gender': '',
                'time': '',
                'runs': 0, # Default to 0 instead of checking for a specific column
                'open': '',
                'is_pb': False
            }
            return

        if self.in_row:
            # Check for explicit PB marker classes
            if 'pbc' in classes.split() or 'Results-table-td--pb' in classes:
                self.current_row['is_pb'] = True

            # 2. Flag which field we are currently reading
            if 'Results-table-td--position' in classes:
                self.current_field = 'position'
            elif 'Results-table-td--name' in classes:
                self.current_field = 'name'
            elif 'Results-table-td--gender' in classes:
                self.current_field = 'gender'
            elif 'Results-table-td--time' in classes:
                self.current_field = 'time'

    def handle_data(self, data):
        # Extract metadata from <title>
        if self.in_title:
            self.event_title += data
            return

        # 3. Process row data dynamically
        if self.in_row:
            clean_data = data.strip()
            if clean_data:
                # Detect specific achievement text for new PBs
                if re.search(r'\b(nowy\s+pb!?|new\s+pb!?)\b', clean_data, re.IGNORECASE):
                    self.current_row['is_pb'] = True

                # Extract number of runs from text anywhere in the row (e.g., "150 parkruns", "50 parkrunów")
                run_match = re.search(r'\b(\d+)\s+Ukończone edycje', clean_data, re.IGNORECASE)
                if run_match:
                    self.current_row['runs'] = int(run_match.group(1))
                    
                    # Prevent the run count from appending to text fields like 'name'
                    clean_data = re.sub(r'\b\d+\s+parkrun\w*', '', clean_data, flags=re.IGNORECASE).strip()
                    if not clean_data:
                        return 

                # Capture text for tracked fields
                if self.current_field:
                    if self.current_row[self.current_field]:
                        self.current_row[self.current_field] += " " + clean_data
                    else:
                        self.current_row[self.current_field] = clean_data

    def handle_endtag(self, tag):
        # Stop tracking <title> tag
        if tag == 'title':
            self.in_title = False

        # 4. Turn off the field flag when leaving containers to prevent spillover
        if self.in_row and tag in ('td', 'div', 'span'):
            self.current_field = None

        # 5. Save and reset at the end of the row
        if tag == 'tr' and self.in_row:
            # Clean up raw text
            self.current_row['name'] = self.current_row['name'].split("  ")[0].strip() or "Unknown"
            self.current_row['gender'] = self.current_row['gender'].split("\n")[0].strip() or "Unknown"
            
            # Clean time string
            raw_time = self.current_row['time'].split("\n")[0].strip() or "N/A"
            cleaned_time = re.sub(r'(?i)(nowy\s+)?pb!?|\bnew\s+pb!?', '', raw_time).strip()
            self.current_row['time'] = cleaned_time

            if self.current_row['gender'].startswith('M'):
                self.m_pos += 1
                self.current_row['open'] = self.m_pos
            elif self.current_row['gender'].startswith('K'):
                self.f_pos += 1
                self.current_row['open'] = self.f_pos

            self.results.append(self.current_row)

            self.in_row = False
            self.current_row = None
            self.current_field = None

    def get_event_name(self):
        """Parses event name from extracted title string."""
        if '|' in self.event_title:
            return self.event_title.split('|')[-1].strip()
        return self.event_title.strip() or "Unknown Event"

def get_edition_from_url(url):
    """Extracts the edition/event number from the URL path."""
    segments = [seg for seg in urlparse(url).path.split('/') if seg]
    return segments[2] if len(segments) > 2 else "Unknown"

def get_parkrun_results(url):
    req = Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )

    with urlopen(req) as response:
        return response.read().decode('utf-8')

def check_pb(is_pb):
    return " 🔥 PB!" if is_pb else ""

def check_milestone(runs):
    """Checks if a runner has achieved a parkrun milestone."""
    if runs in [10, 25, 50, 100, 250, 500, 1000]:
        return f" 👕 {runs} parkrunów! 👏"
    elif runs > 100 and runs % 50 == 0:
        return f" 🎈 {runs} parkrunów! 👏"
    return ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <parkrun_url>")
        sys.exit(1)

    target_url = sys.argv[1]
    
    html_data = get_parkrun_results(target_url)
    parser = ParkrunParser()
    parser.feed(html_data)
    edition = sys.argv[1].strip('/').split('/')[-1]

    print(f"🌳 {parser.get_event_name()} #{edition}")
    for r in parser.results:
        name = get_team_member(r['name'])
        if name is None:
            continue

        pb_badge = check_pb(r['is_pb'])
        milestone_badge = check_milestone(r['runs'])

        print(f"{name} {gender_icon(r['gender'][0])} {r['position']}/{len(parser.results)} ⏱️{r['time']} {get_award(r['open'])}{pb_badge}{milestone_badge}")

    print(f"🔗 {target_url}")
