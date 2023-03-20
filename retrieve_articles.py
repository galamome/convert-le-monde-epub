import io
import shutil
import tempfile
import urllib.request
from lxml import etree
import asyncio
import os.path
import aiofiles
import aiohttp

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
                    "//div[@id='Header']",
                    "//div[@id='cover']",
                    "//div[@id='dfp-habillage']",
                    "//div[@id='banniere_haute']",
                    "//ul[@class='meta meta__social   old__meta-social meta__social--gift']",
                    "//section[@id='js-message-register']",
                    "//div[@class='lazy-bizdev']",
                    "//div[@id='overlay']",
                    "//span[@class='sr-only']",
                    "//div[@class='lmd-dropdown__overlay']",
                    "//ul[@class='meta meta__social  meta__social--opinion old__meta-social meta__social--gift']"
                    #,"//span[@class='meta__article-en-fr-url-link'", "//span[@class='icon__premium'"
                    ]

########################################################################
# Functions
########################################################################

def remove_unnecessary_elements(xml_tree, to_be_removed_xpaths):
    # Loop through of XPath to be removed
    for xpath in to_be_removed_xpaths:
        # Remove particular elements
        for s in xml_tree.xpath(xpath):
            s.getparent().remove(s)
    return xml_tree

async def get_and_convert_le_monde_article(articleUrl, cookie):
    splittedUrl = articleUrl.split('/')

    lastIndex = len(splittedUrl) - 1
    htmlFileName = f'{splittedUrl[lastIndex-3]}_{splittedUrl[lastIndex-2]}_{splittedUrl[lastIndex-1]}_{splittedUrl[lastIndex]}'
    nakedFileName = htmlFileName.split('.')[0]

    # Limit the file name size
    nakedFileName = nakedFileName[:35]

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

                without_script = etree.tostring(tree.getroot(), encoding='unicode', method='xml')

                # Write file
                async with aiofiles.open(htmlFileName, "w") as text_file:
                    await text_file.write(without_script)
    else:
        print(f'File {htmlFileName} already exists, and article {articleUrl} will NOT be written')

##########################################

myCookie = "lmd_gdpr_token=1; atauthority=%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22cnil%22%2C%22visitor_mode%22%3A%22exempt%22%7D%2C%22options%22%3A%7B%22end%22%3A%222024-04-19T10%3A01%3A22.394Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidx=20E50FC4-85A0-49A7-B48F-AC3A21509C5F; atid=20E50FC4-85A0-49A7-B48F-AC3A21509C5F; lmd_sso_twipe=%7B%22token%22%3A%22SrWrUiyFGMNI4QIoA49%5C%2FxiAOOuh06HZLaDsvqrJiujE%3D%22%7D; lmd_a_s=2XZdAdv51r0S15vcazvfPrByZ7GHggmU1Xlog4os0GwLeh2cXvmhHG3uFKoWf2AE; lmd_a_ld=cq%2FED61uukL7lcpak8TTaiZs9zIClG4B15G0HFJLvg0%3D; lmd_a_sp=2XZdAdv51r0S15vcazvfPrByZ7GHggmU1Xlog4os0GwLeh2cXvmhHG3uFKoWf2AE; lmd_stay_connected=0; lmd_a_m=SrWrUiyFGMNI4QIoA49%2FxiAOOuh06HZLaDsvqrJiujE%3D; euconsent-v2=CPdnuOJPdnuOJFzABCFRBdCgAAAAAAAAAAAAAAAAAAAA; lmd_consent=%7B%22userId%22%3A%228ce667c9-04da-4f5f-a51a-ca901765e8c2%22%2C%22timestamp%22%3A%221660307956.152987654%22%2C%22version%22%3A1%2C%22cmpId%22%3A371%2C%22displayMode%22%3A%22subscriber%22%2C%22purposes%22%3A%7B%22analytics%22%3Afalse%2C%22ads%22%3Afalse%2C%22personalization%22%3Afalse%2C%22mediaPlatforms%22%3Afalse%2C%22social%22%3Afalse%7D%7D; lmd_cap=_q7qieqqqk; lmd_a_c=1; lmd_ab=UgbDLT9lDzbt5hZhsq%2BccSlNC3R98yLL7kEM78XDi7ZuCASPgLzk%2BxHK6Le%2FioBaGc63m%2FA9KnW%2FsbBlQhg6FP8RdtTU3l29f5TYaqX%2B5vRWJ4pqo1ZuoF4iDgrNbrnji1UH%2BUSleY2oBP09ZVqbugxvUSYt4yfJkfOfAOU%3D"


async def main():
    f = open("Articles_fevrier.txt", "r")
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
