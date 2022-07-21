# Get xpath according to url and keyword.

import requests
from lxml import etree

# Set the url
url = 'https://www.sciencenews.org/'

# Set the keyword
kw = 'Dogs'

# Set the starting point
xpath = '/html/body//*/text()'

resp = requests.get(url)
resp.encoding = 'utf-8'
html = etree.HTML(resp.text)


# Define a function that can go deep to search the keyword
def deeper(html, xpath):
    # Update the path to the child nodes
    xpath = xpath.replace('//', '/div//')
    text = html.xpath(xpath)

    # Search for the keyword in every element
    for i in text:
        if kw in i:
            return True
    return False


# Define a function that can check sibling nodes
def wider(html, xpath):
    # Set the starting point of sibling node
    n = 1
    while True:
        # Update current path to a certain child node
        xpath = xpath.replace('//', f'/div[{n}]//')
        text = html.xpath(xpath)

        # Search for the keyword in every element
        for i in text:
            # If the keyword is in current path, return the path
            if kw in i:
                print(f'Update xpath：{xpath}')
                return xpath

        # Can't find the keyword, back to the parent node and ready for the next child note
        xpath = xpath.replace(f'/div[{n}]//', '//')
        n += 1


if __name__ == '__main__':
    while True:
        # Search the keyword in child nodes
        if deeper(html, xpath):
            # Found the keyword, update the new path
            xpath = wider(html, xpath)
        else:
            # Can't find it. The current path is the xpath
            print("Can't go deeper.")
            break
    print(f'The keyword is somewhere in the following path：\n{xpath}')
    print(html.xpath(xpath))

resp.close()