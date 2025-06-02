import pandas as pd
from difflib import SequenceMatcher
import re
import sqlite3

db = sqlite3.connect("results.db")
lines = []
for row in db.cursor().execute("SELECT name FROM results"):
    lines.append(row[0])

# Define a function to calculate similarity ratio between two strings
def similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to normalize strings for better comparison
def normalize_string(s):
    # Convert to lowercase, replace Polish characters with ASCII equivalents
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z'
    }
    s_lower = s.lower()
    for polish, ascii in replacements.items():
        s_lower = s_lower.replace(polish, ascii)
    # Remove hyphens and extra spaces
    s_lower = re.sub(r'[-\s]+', ' ', s_lower).strip()
    return s_lower

# Parse names into surname and first name components
parsed_names = []
for line in lines:
    parts = line.split()
    if len(parts) >= 2:
        surname = parts[0]
        first_name = ' '.join(parts[1:])
        parsed_names.append((line, surname, first_name))

# Find exact duplicates
exact_duplicates = []
seen = set()
for line in lines:
    if line in seen:
        exact_duplicates.append(line)
    else:
        seen.add(line)

# Check for similar names based on components
similar_names = []
for i, (line_i, surname_i, first_i) in enumerate(parsed_names):
    for j, (line_j, surname_j, first_j) in enumerate(parsed_names):
        if i >= j:  # Skip self-comparisons and duplicates
            continue
            
        # Skip exact matches
        if line_i == line_j:
            continue
            
        # Check surname similarity
        surname_sim = similarity_ratio(surname_i, surname_j)
        # Check first name similarity
        first_sim = similarity_ratio(first_i, first_j)
        
        # Case 1: Very similar surnames with identical first names
        if surname_sim > 0.8 and first_i == first_j:
            similar_names.append((line_i, line_j, "Similar surname, identical first name", surname_sim))
        
        # Case 2: Identical surnames with very similar first names
        elif surname_i == surname_j and first_sim > 0.8:
            similar_names.append((line_i, line_j, "Identical surname, similar first name", first_sim))
        
        # Case 3: Both components are somewhat similar (likely typos in both)
        elif surname_sim > 0.7 and first_sim > 0.7:
            overall_sim = (surname_sim + first_sim) / 2
            similar_names.append((line_i, line_j, "Similar in both components", overall_sim))
        
        # Case 4: High overall similarity but not caught by above rules
        else:
            overall_sim = similarity_ratio(line_i, line_j)
            if overall_sim > 0.9:
                similar_names.append((line_i, line_j, "High overall similarity", overall_sim))

# Check for special cases: BŁASZCZAK/BLASZCZAK pattern and similar
special_cases = []
for i, (line_i, surname_i, first_i) in enumerate(parsed_names):
    for j, (line_j, surname_j, first_j) in enumerate(parsed_names):
        if i >= j:
            continue
            
        # Check if names differ only in Polish vs. non-Polish characters
        normalized_i = normalize_string(line_i)
        normalized_j = normalize_string(line_j)
        
        if normalized_i == normalized_j and line_i != line_j:
            special_cases.append((line_i, line_j, "Differs only in Polish characters"))

# Sort by similarity score
similar_names.sort(key=lambda x: x[3], reverse=True)

# Output results
print("1. Exact duplicates found:")
if exact_duplicates:
    for dup in sorted(set(exact_duplicates)):
        print(f"   - {dup}")
else:
    print("   No exact duplicates found.")

print("\n2. Names differing only in Polish characters:")
if special_cases:
    for name1, name2, reason in special_cases:
        print(f"   - {name1} <-> {name2}")
else:
    print("   No such cases found.")

print("\n3. Most similar name pairs:")
for name1, name2, reason, score in similar_names[:15]:
    print(f"   - {name1} <-> {name2} ({reason}, score: {score:.4f})")
