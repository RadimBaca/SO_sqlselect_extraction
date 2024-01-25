import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def scrape_fiddles(input_file, output_folder, link_prefix, fiddle_num_in_one_file):
    # Read links from the input file starting with the specified prefix
    with open(input_file, 'r') as file:
        links = [line.strip() for line in file if line.startswith(link_prefix)]

    # Create a counter to keep track of the number of fiddles
    fiddle_count = 0

    # Iterate through each link and scrape the content
    for link_num, link in enumerate(links, start=1):
        if (link_num % 100) == 0:
            print("Link num: " + str(link_num))

        response = requests.get(link)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <div> elements with class "input"
            input_divs = soup.find_all('div', class_='input')

            # Create a fiddle element with a link attribute
            fiddle_element = ET.Element("fiddle", link=link)

            # Iterate through each input_div and create a div subelement
            for index, div in enumerate(input_divs):
                div_content = div.get_text(strip=True)

                # Create a div subelement with data-markdown attribute
                div_element = ET.SubElement(fiddle_element, "div", data_markdown=div_content)

            # Create an ElementTree from the fiddle element
            tree = ET.ElementTree(fiddle_element)

            # Check if it's time to create a new XML file (every 1000 fiddles)
            if fiddle_count % fiddle_num_in_one_file == 0:
                # Generate the output file name with a number
                output_file = f"{output_folder}/output_{fiddle_count // fiddle_num_in_one_file}.xml"

                # Write the ElementTree to the XML file
                tree.write(output_file)
            else:
                # Append the fiddle element to the existing XML file
                existing_tree = ET.parse(output_file)
                existing_root = existing_tree.getroot()
                existing_root.append(fiddle_element)
                existing_tree.write(output_file)

            fiddle_count += 1

        else:
            print(f"Failed to retrieve the page for link {link}. Status code: {response.status_code}")

# Example usage
input_file_path = 'fiddles.txt'
output_folder_path = 'fiddles_xml'
prefix_to_match = 'https://dbfiddle.uk'
fiddle_num_in_one_file = 500
scrape_fiddles(input_file_path, output_folder_path, prefix_to_match, fiddle_num_in_one_file)
