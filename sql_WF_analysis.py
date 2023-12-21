import re
import html
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime

if len(sys.argv) < 2:
	print("Please provide a path to a queries.txt file")
	sys.exit()

path = sys.argv[1]

if not os.path.exists(path):
	print(f"The path '{path}' does not exist.")
	sys.exit()


regex = r'\bSELECT\b.*\)\s*OVER\s*\('

# win func per 1000 statements
window_functions = {
    'ROW_NUMBER': r'\bROW_NUMBER\s*\(\s*\)\s*OVER\s*\(',
    'RANK': r'\bRANK\s*\(\s*\)\s*OVER\s*\(',
    'DENSE_RANK': r'\bDENSE_RANK\s*\(\s*\)\s*OVER\s*\(',
    'LAG': r'\bLAG\s*\(\s*.+?\s*\)\s*OVER\s*\(',
    'LEAD': r'\bLEAD\s*\(\s*.+?\s*\)\s*OVER\s*\(',
    'MAX': r'\bMAX\s*\(\s*.+?\s*\)\s*OVER\s*\(',
    'MIN': r'\bMIN\s*\(\s*.+?\s*\)\s*OVER\s*\(',
    'AVG': r'\bAVG\s*\(\s*.+?\s*\)\s*OVER\s*\(',
    'SUM': r'\bSUM\s*\(\s*.+?\s*\)\s*OVER\s*\(',
    'COUNT': r'\bCOUNT\s*\(\s*.+?\s*\)\s*OVER\s*\(',
    'FIRST_VALUE': r'\bFIRST_VALUE\s*\(\s*.+?\s*\)\s*OVER\s*\(',
    'LAST_VALUE': r'\bLAST_VALUE\s*\(\s*.+?\s*\)\s*OVER\s*\('
}

y_all = []
x_all = []
wf_counter = 0

y = {func: [] for func in window_functions}
wf_counters = {func: 0 for func in window_functions}
wf_colors = {}

for func in window_functions:
    c = [random.randint(0, 4) / 5,
        random.randint(0, 4) / 5,
        random.randint(0, 4) / 5]
    r = random.randint(0,2)
    c[r] = min(c[r] * 2, 1.0)
    wf_colors[func] = (c[0], c[1], c[2])

prev_date = '2008-08'
counter = 0
x_values = []
x_year_month = []
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        counter += 1
        actual_date = line[:7]

        if re.search(regex, line, re.IGNORECASE):
            wf_counter += 1
            for func, func_regex in window_functions.items():
                if re.search(func_regex, line, re.IGNORECASE):
                    wf_counters[func] += 1

        if actual_date != prev_date:
            try:
                year = actual_date[:4]
                month = actual_date[5:7]
                if (int(year) >= 2008 and int(year) <= 2019) and (int(month) >= 1 and int(month) <= 12):
                    y_all.append(wf_counter)
                    x_all.append(counter)
                    x_year_month.append(datetime.strptime(actual_date, "%Y-%m"))
                    wf_counter = 0
                    counter = 0
                    for func in window_functions:
                        y[func].append(wf_counters[func])
                        wf_counters[func] = 0
            except ValueError:
                continue

        prev_date = actual_date

print(sum(y_all))
print(counter)



x_percent = []
y_percent = []
for i in range(0, len(y_all)):
    if float(y_all[i])/x_all[i]*100.0 > 20: # there is one outlier we do not want to plot
        continue
    y_percent.append(float(y_all[i])/x_all[i]*100.0)
    x_percent.append(x_year_month[i])


plt.scatter(x_percent, y_percent, s=10)
# Add labels and title
plt.xlabel('Time [Year-Month]')
plt.ylabel('Queries with window function [%]')

# # Add trendline
z = np.polyfit(plt.matplotlib.dates.date2num(x_percent), y_percent, 2) # 2 represents the degree of the polynomial
p = np.poly1d(z)
plt.plot(x_percent,p(plt.matplotlib.dates.date2num(x_percent)),"r--",  color='blue')

plt.xticks(rotation=45, ha='right')
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))


# for func in window_functions:
#     z = [y[func][i]/10 for i in range(0, len(y[func]))]
#     #plt.scatter(x, z, s=10, color=[wf_colors[func] for i in range(0, len(z))])
#     w = np.polyfit(x, z, 2) # 2 represents the degree of the polynomial
#     p = np.poly1d(w)
#     plt.plot(x,p(x),"r--",color=wf_colors[func])
#
# plt.legend(['All', 'Trendline All'] + [func for func in window_functions])

plt.subplots_adjust(left=0.1, right=0.97, top=0.94, bottom=0.2)  # Adjust the values as per your requirements
plt.show()


# Create the bar plot
plt.bar([func for func in window_functions], [sum(y[func]) for func in window_functions],color=[wf_colors[func] for func in window_functions])
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(left=0.12, right=0.97, top=0.94, bottom=0.2)  # Adjust the values as per your requirements

# Set the title and axis labels
# plt.title('Occurence of each Window Function')
plt.xlabel('Window Function')
plt.ylabel('Occurences')

plt.show()