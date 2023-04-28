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

select_from_regex = r'&lt;code&gt;SELECT\s.*?FROM\s.*?&lt;/code&gt;'
counter = 0

with open(path, 'r', encoding='utf-8') as f:
    with open('sqlcommands.txt', 'w', encoding='utf-8') as outfile:  # opening a new file to write output
        for line in f:
            try:
                matches = re.findall(select_from_regex, line)
                for match in matches:
                    counter += 1
                    if (counter % 10000) == 0:
                        print(counter)
                    without_comments = re.sub('--.*?&#xA;', '', match)
                    output_string = html.unescape(html.unescape(without_comments.replace('&#xA;', ' '))).replace('<code>','').replace('</code>','')
                    outfile.write(output_string+'\n')  # writing output to file
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}")
