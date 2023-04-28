import re
import html
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) < 2:
	print("Please provide a path to a queries.txt file")
	sys.exit()

path = sys.argv[1]

if not os.path.exists(path):
	print(f"The path '{path}' does not exist.")
	sys.exit()


regex = r'\bSELECT\b.*\bOVER\s*\('

# win func per 1000 statements
y = []

counter = 0
wf_counter = 0
with open(path, 'r', encoding='utf-8') as f:
	for line in f:
		counter += 1
		if re.search(regex, line):
			wf_counter += 1

		if (counter % 1000) == 0:
			y.append(wf_counter)
			wf_counter = 0
			

# Print the number of statements with window functions
print(sum(y))
# Print the number of statements
print(counter)

# Print number of queries with window function per 1000 queries
# for i in range(len(y)):
#    print(y[i])
x = [i for i in range(0, len(y))]
y = [y[i]/10 for i in range(0, len(y))]
plt.scatter(x, y, s=10)
# Add labels and title
plt.xlabel('Queries')
plt.ylabel('Queries with window function [%]')
# plt.title('X-Y Plot')


# Add trendline
z = np.polyfit(x, y, 2) # 2 represents the degree of the polynomial
p = np.poly1d(z)
plt.plot(x,p(x),"r--")

# Show plot
plt.show()