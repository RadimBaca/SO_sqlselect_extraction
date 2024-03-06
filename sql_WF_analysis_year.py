import re
import html
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

if len(sys.argv) < 2:
    print("Please provide a path to a queries.txt file")
    sys.exit()

path = sys.argv[1]

if not os.path.exists(path):
    print(f"The path '{path}' does not exist.")
    sys.exit()


regex = r'\bSELECT\b.*\)\s*OVER\s*\('

wf_all = []  # Dictionary to store yearly counts
years = []

prev_year = None
current_year = None
wf_counter = 0
counter = 0
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        counter += 1
        current_year = line[:4]

        try:
            if prev_year == None:
                prev_year = int(current_year)

            if int(current_year) >= 2008 and int(current_year) <= 2023 :
                current_year = int(current_year)
                if re.search(regex, line, re.IGNORECASE):
                    wf_counter += 1

                if current_year != prev_year:
                    wf_all.append(float(wf_counter) / counter * 100)
                    years.append(prev_year)
                    wf_counter = 0 
                    counter = 0
                    prev_year = current_year
        except ValueError:
            continue

    # Add count for the last year
    if wf_counter > 0:	
        wf_all.append(float(wf_counter) / counter * 100)
        years.append(prev_year)

print(years)
print(wf_all)


# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(years, wf_all, color='skyblue')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Queries with WFE [%]')

# Rotate x-axis labels for better readability
# plt.xticks(rotation=45, ha='right')

# Show plot
plt.show()
