import io
import shutil
import tempfile
import urllib.request
from lxml import etree

urlToRetrieve = "https://www.lemonde.fr/international/article/2023/02/13/alexei-venediktov-la-haine-est-entree-au-sein-de-chaque-famille-russe_6161602_3210.html"
cookie = "lmd_gdpr_token=1; atauthority=%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22cnil%22%2C%22visitor_mode%22%3A%22exempt%22%7D%2C%22options%22%3A%7B%22end%22%3A%222024-04-12T17%3A11%3A46.983Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidx=20E50FC4-85A0-49A7-B48F-AC3A21509C5F; atid=20E50FC4-85A0-49A7-B48F-AC3A21509C5F; lmd_sso_twipe=%7B%22token%22%3A%22SrWrUiyFGMNI4QIoA49%5C%2FxiAOOuh06HZLaDsvqrJiujE%3D%22%7D; lmd_a_s=2XZdAdv51r0S15vcazvfPrByZ7GHggmU1Xlog4os0GwLeh2cXvmhHG3uFKoWf2AE; lmd_a_ld=cq%2FED61uukL7lcpak8TTaiZs9zIClG4B15G0HFJLvg0%3D; lmd_a_sp=2XZdAdv51r0S15vcazvfPrByZ7GHggmU1Xlog4os0GwLeh2cXvmhHG3uFKoWf2AE; lmd_stay_connected=0; lmd_a_m=SrWrUiyFGMNI4QIoA49%2FxiAOOuh06HZLaDsvqrJiujE%3D; euconsent-v2=CPdnuOJPdnuOJFzABCFRBdCgAAAAAAAAAAAAAAAAAAAA; lmd_consent=%7B%22userId%22%3A%228ce667c9-04da-4f5f-a51a-ca901765e8c2%22%2C%22timestamp%22%3A%221660307956.152987654%22%2C%22version%22%3A1%2C%22cmpId%22%3A371%2C%22displayMode%22%3A%22subscriber%22%2C%22purposes%22%3A%7B%22analytics%22%3Afalse%2C%22ads%22%3Afalse%2C%22personalization%22%3Afalse%2C%22mediaPlatforms%22%3Afalse%2C%22social%22%3Afalse%7D%7D; lmd_cap=_q7qieqqqk; lmd_ab=hHupglDtCPSH8wIk3cUj8EEik%2F97FceyGGTP%2FghGCGZQyt9yg6LoPbrWWvbw9SxAHnRJL12fmdsTe%2BGZUJjy9Pj8id0T6pc6m9JZNoeb5GY%2BJ1ffOwBBW8McaVQPwE86RQvFxMyueC4GSxFUMXwrh7FM4TWSSOwS0v0ZqaQGxrH%2FH4oUw2spHH9svjfNQheM80VUlKIaGvE8q1TmHA%3D%3D; lmd_a_c=1"
splittedUrl = urlToRetrieve.split('/')

lastIndex = len(splittedUrl) - 1

fileName = f'{splittedUrl[lastIndex-3]}_{splittedUrl[lastIndex-2]}_{splittedUrl[lastIndex-1]}_{splittedUrl[lastIndex]}'

a_request = urllib.request.Request(urlToRetrieve)

a_request.add_header("Cookie", cookie)
with urllib.request.urlopen(a_request) as response:
    content_char_set = response.headers.get_content_charset()
    the_page =  response.read().decode(response.headers.get_content_charset())

    # Replace attribute not allowed
    # Attribute name "crossorigin" associated with an element type "link" must be followed by the ' = ' character. 
    modified = the_page.replace(" crossorigin>", " crossorigin=\"anonymous\">")

    parser = etree.HTMLParser()
    tree = etree.parse(io.StringIO(modified), parser)

    # Remove <script elements
    for s in tree.xpath('//script'):
        s.getparent().remove(s)
    for s in tree.xpath('//link'):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//section[@class='catcher catcher--inline']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//section[@class='article__reactions']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//section[@class='inread js-services-inread']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//footer[@class='article__footer-single old__article-footer']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//aside[@class='aside__iso   old__aside']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//footer[@class='footer footer--abo old__footer']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//section[@id='js-capping']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//section[@id='js-capping-old-article']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//div[@class='Header__nav-container']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//div[@id='Header']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//div[@id='cover']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//div[@id='dfp-habillage']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//div[@id='banniere_haute']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//ul[@class='meta meta__social   old__meta-social meta__social--gift']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//section[@id='js-message-register']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//div[@class='lazy-bizdev']"):
        s.getparent().remove(s)
    # Remove particular elements
    for s in tree.xpath("//div[@id='overlay']"):
        s.getparent().remove(s)


    without_script = etree.tostring(tree.getroot(), encoding='UTF-8')

    text_file = open(fileName, "wb")
    n = text_file.write(without_script)
    text_file.close()

    # process Unicode text
    #with io.open(fileName,'w',encoding='utf8') as f:
     #   f.write(without_script)



# A prendre
#  <article class="article__content old__article-content-single">
# //article[@class='article__content old__article-content-single']
