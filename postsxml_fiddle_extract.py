import re
import html
import os
import sys


if len(sys.argv) < 2:
    print("Please provide a path as a command line argument.")
    sys.exit()

path = sys.argv[1]

if not os.path.exists(path):
    print(f"The path '{path}' does not exist.")
    sys.exit()

# List of supported URLs
supported_urls = [
    "https://www.db-fiddle.com/",
    "https://dbfiddle.uk/",
    "https://sqlfiddle.com/"
]

# Create regex patterns for each supported URL
regex_patterns = [rf'href=&quot;({re.escape(url)}\S+)&quot;' for url in supported_urls]

with open(path, 'r', encoding='utf-8') as f:
    with open('fiddles.txt', 'w', encoding='utf-8') as outfile:  # opening a new file to write output
        for line_number, line in enumerate(f, start=1):
            try:
                if (line_number % 1000000) == 0:
                    print("Line number: " + str(int(line_number / 1000000)) + "M")
                for regex_pattern in regex_patterns:
                    matches = re.findall(regex_pattern, line)
                    for match in matches:
                        print(html.unescape(html.unescape(match)))
                        outfile.write(html.unescape(html.unescape(match)) + '\n')  # writing output to file
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}")




