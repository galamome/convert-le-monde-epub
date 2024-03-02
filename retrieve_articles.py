import io
import shutil
import tempfile
import urllib.request
from lxml import etree
from typing import List
import asyncio
import os.path
import aiofiles
import aiohttp
import argparse


######################################################
# Constants
######################################################

TO_REMOVE_XPATHS = ['//title',
                    '//script',
                    '//noscript',
                    '//link',
                    "//section[@class='catcher catcher--inline']",
                    "//section[@class='article__reactions']",
                    "//section[@class='inread js-services-inread']",
                    "//footer[@class='article__footer-single old__article-footer']",
                    "//aside[@class='aside__iso   old__aside']",
                    "//footer[@class='footer footer--abo old__footer']",
                    "//section[@id='js-capping']",
                    "//section[@id='js-capping-old-article']",
                    "//div[@class='Header__nav-container']",
                    "//div[@class='article__gift-modal__title']"
                    "//div[@id='Header']",
                    "//div[@id='cover']",
                    "//div[@id='dfp-habillage']",
                    "//div[@id='banniere_haute']",
                    "//ul[@class='meta meta__social   old__meta-social meta__social--gift']",
                    "//section[@id='js-message-register']",
                    "//div[@class='lazy-bizdev']",
                    "//div[@id='overlay']",
                    "//section[@class='inread inread--NL js-services-inread']",
                    "//div[@class='inread__headline']",
                    "//div[@class='catcher__content']",
                    "//div[@class='catcher__favorite']",
                    "//span[@class='sr-only']",
                    "//section[@class='paywall js-paywall paywall--longform paywall--abo']",
                    "//div[@class='lmd-dropdown__overlay']",
                    "//ul[@class='meta meta__social  meta__social--opinion old__meta-social meta__social--gift']",
                    "//button[@aria-label='Ajouter à vos sélections']",
                    "//h3[@class='footer__category-title']",
                    "//footer[@class='footer footer--abo']",
                    "//ul[@class='footer__links']",
                    "//section[@class='services-carousel']",
                    "//div[@id='Header']",
                    "//div[@id='js-modal-gifted-url']",
                    "//p[@class='article__status']",
                    "//ul[@class='meta meta__social   meta__social--gift']"
                    #,"//span[@class='meta__article-en-fr-url-link'", "//span[@class='icon__premium'"
                    ]

########################################################################
# Functions
########################################################################

def parse_args():
    parser=argparse.ArgumentParser(description="A script to retrieve Le Monde articles")
    parser.add_argument("--articleFile",
                        type=str,
                        default="articles.txt",
                        help='fichier liste des articles')
    parser.add_argument("--cookie",
                        type=str,
                        help='cookie doit être entouré de guillemets double')
    args=parser.parse_args()
    return args

def remove_unnecessary_elements(xml_tree: etree._ElementTree, to_be_removed_xpaths: List[str]) -> etree._ElementTree:
    """
    Return the tree modified, without all the elements
    that match the XPath passed as "to_be_removed_xpaths" parameter

    Parameters:
    -----------
    xml_tree: etree._ElementTree
        the tree in input
    to_be_removed_xpaths: List[str]
        list of XPath of elements to be removed

    Returns:
    --------
    tree: etree._ElementTree
        the tree modified.
    """
    # Loop through of XPath to be removed
    for xpath in to_be_removed_xpaths:
        # Remove particular elements
        for s in xml_tree.xpath(xpath):
            s.getparent().remove(s)
    return xml_tree

def repair_image_elements(xml_tree: etree._ElementTree) -> etree._ElementTree:
    """
    Return the tree modified, without "img" elements
    that have "data-srcset" attribute.
    Replace them by "srcset" attribute with the same value.
    Same thing with "data-sizes" and "sizes"

    Parameters:
    -----------
    xml_tree: etree._ElementTree
        the tree in input

    Returns:
    --------
    tree: etree._ElementTree
        the tree modified.
    """
    # Remove particular elements
    for s in xml_tree.xpath('//img'):
        #for val in s.attrib:
#            print(f'Value of each attribute {val}, {s.attrib[val]}')
        if 'data-srcset' in s.attrib:
            #print(f'Content of data-srcset attribute was {s.attrib["data-srcset"]}')
            s.attrib["srcset"] = s.attrib["data-srcset"]
            s.attrib.pop("data-srcset")
        if 'data-sizes' in s.attrib:
            #print(f'Content of data-sizes attribute was {s.attrib["data-sizes"]}')
            s.attrib["sizes"] = s.attrib["data-sizes"]
            s.attrib.pop("data-sizes")            
            
        #print(f'Content of img element is {s.attrib}')
    return xml_tree

async def get_and_convert_le_monde_article(articleUrl, cookie):
    splittedUrl = articleUrl.split('/')

    lastIndex = len(splittedUrl) - 1
    articleDescription = splittedUrl[lastIndex].replace("-", "_")
    htmlFileName = f'{splittedUrl[lastIndex-3]}{splittedUrl[lastIndex-2]}{splittedUrl[lastIndex-1]}-{articleDescription}'
    nakedFileName = htmlFileName.split('.')[0]

    # Limit the file name size
    nakedFileName = nakedFileName[:40]

    htmlFileName = f'{nakedFileName}.html'

    headers={"Cookie": cookie}
    if not os.path.exists(htmlFileName):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(articleUrl) as response:
                content_char_set = response.get_encoding()
                the_page = await response.text()

                # Replace attribute not allowed
                # Attribute name "crossorigin" associated with an element type "link" must be followed by the ' = ' character. 
                modified = the_page.replace(" crossorigin>", " crossorigin=\"anonymous\">")

                parser = etree.HTMLParser()
                tree = etree.parse(io.StringIO(modified), parser)

                # Remove all unnecessary elements from the HTML, based on XPath
                tree = remove_unnecessary_elements(tree, TO_REMOVE_XPATHS)

                # Repair image reference (replace data-srcset & data-sizes in "img" element)
                tree = repair_image_elements(tree)

                without_script = etree.tostring(tree.getroot(), encoding='unicode', method='xml')

                # Write file
                async with aiofiles.open(htmlFileName, "w") as text_file:
                    await text_file.write(without_script)
    else:
        print(f'File {htmlFileName} already exists, and article {articleUrl} will NOT be written')

##########################################
async def main():
    # Retrieve args
    inputs=parse_args()

    articleFileName = inputs.articleFile
    myCookie = inputs.cookie
    print(myCookie)
    f = open(articleFileName, "r")
    urls = set([])
    for line in f.readlines():
        if "https://www.lemonde.fr/" in line:
            # Since it is a set, will only be added once
            urls.add(line)
    for url in urls:
        await get_and_convert_le_monde_article(url, myCookie)

asyncio.run(main())
        #command_to_convert_to_epub = convert(articleName)

        # Run the command to run "pandoc"
        #asyncio.run(run(command_to_convert_to_epub))
