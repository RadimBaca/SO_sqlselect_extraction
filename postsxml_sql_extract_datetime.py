import re
import html
import os
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) < 2:
    print("Please provide a path as a command line argument.")
    sys.exit()

path = sys.argv[1]

if not os.path.exists(path):
    print(f"The path '{path}' does not exist.")
    sys.exit()

select_from_regex = r'<row.*?CreationDate="(.*?)'
original_sql_regex = r'&lt;code&gt;SELECT\s.*?FROM\s.*?&lt;/code&gt;'
counter = 0

with open(path, 'r', encoding='utf-8') as f:
    with open('sqlcommands.txt', 'w', encoding='utf-8') as outfile:  # opening a new file to write output
        for line in f:
            try:
                # matches_creation_date = re.findall(select_from_regex, line)
                creation_date_regex = r'CreationDate="([^"]+)"'
                creation_date_match = re.search(creation_date_regex, line)

                # if creation_date_match:
                    # creation_date_value = creation_date_match.group(1)
                    # print(f"Creation Date: {creation_date_value}")
                # else:
                    # print("Creation Date not found.")

                matches_original_sql = re.findall(original_sql_regex, line)

                for match in matches_original_sql:
                    counter += 1
                    if (counter % 10000) == 0:
                        print(counter)
                    without_comments = re.sub('--.*?&#xA;', '', match)
                    output_string = html.unescape(html.unescape(without_comments.replace('&#xA;', ' '))).replace(
                        '<code>', '').replace('</code>', '')
                    # outfile.write(output_string + '\n')  # writing output to file for original SQL SELECT FROM pattern
                    outfile.write(f"{creation_date_match.group(1)[:10]}, {output_string}\n")  # writing output to file
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}")
