import re
import html
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import random

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
    'LAST_VALUE': r'\bLAST_VALUE\s*\(\s*.+?\s*\)\s*OVER\s*\(',
    'NTILE': r'\bNTILE\s*\(\s*.+?\s*\)\s*OVER\s*\('
}

y_all = []
wf_counter = 0

y = {func: [] for func in window_functions}
counter = 0
wf_counters = {func: 0 for func in window_functions}
wf_colors = {}

for func in window_functions:
    c = [random.randint(0, 4) / 5,
        random.randint(0, 4) / 5,
        random.randint(0, 4) / 5]
    r = random.randint(0,2)
    c[r] = min(c[r] * 2, 1.0)
    wf_colors[func] = (c[0], c[1], c[2])

with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        counter += 1
        if re.search(regex, line, re.IGNORECASE):
            wf_counter += 1
            for func, func_regex in window_functions.items():
                if re.search(func_regex, line, re.IGNORECASE):
                    wf_counters[func] += 1

        if (counter % 1000) == 0:
            y_all.append(wf_counter)
            wf_counter = 0
            for func in window_functions:
                y[func].append(wf_counters[func])
                wf_counters[func] = 0

# Print the number of statements with window functions
print(sum(y_all))
# Print the number of statements
print(counter)



x = [i for i in range(0, len(y_all))]
y_all = [y_all[i]/10 for i in range(0, len(y_all))]
plt.scatter(x, y_all, s=10)
# Add labels and title
plt.xlabel('# Queries in thousands')
plt.ylabel('Queries with window function [%]')
# plt.title('X-Y Plot')

# Add trendline
z = np.polyfit(x, y_all, 2) # 2 represents the degree of the polynomial
p = np.poly1d(z)
plt.plot(x,p(x),"r--",  color='blue')

for func in window_functions:
    z = [y[func][i]/10 for i in range(0, len(y[func]))]
    #plt.scatter(x, z, s=10, color=[wf_colors[func] for i in range(0, len(z))])
    w = np.polyfit(x, z, 2) # 2 represents the degree of the polynomial
    p = np.poly1d(w)
    plt.plot(x,p(x),"r--",color=wf_colors[func])

plt.legend(['All', 'Trendline All'] + [func for func in window_functions])

# Show plot
plt.show()


# Create the bar plot
plt.bar([func for func in window_functions], [sum(y[func]) for func in window_functions],color=[wf_colors[func] for func in window_functions])

# Set the title and axis labels
# plt.title('Occurence of each Window Function')
plt.xlabel('Window Function')
plt.ylabel('Occurences')
# Rotate x-axis labels
plt.xticks(rotation=45)

# Display the plot
plt.show()