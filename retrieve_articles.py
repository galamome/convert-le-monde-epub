import shutil
import tempfile
import urllib.request

urlToRetrieve = "https://www.lemonde.fr/international/article/2023/02/13/alexei-venediktov-la-haine-est-entree-au-sein-de-chaque-famille-russe_6161602_3210.html"
cookie = "lmd_gdpr_token=1; atauthority=%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22cnil%22%2C%22visitor_mode%22%3A%22exempt%22%7D%2C%22options%22%3A%7B%22end%22%3A%222024-03-16T10%3A37%3A20.863Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidx=20E50FC4-85A0-49A7-B48F-AC3A21509C5F; atid=20E50FC4-85A0-49A7-B48F-AC3A21509C5F; lmd_sso_twipe=%7B%22token%22%3A%22SrWrUiyFGMNI4QIoA49%5C%2FxiAOOuh06HZLaDsvqrJiujE%3D%22%7D; lmd_a_s=2XZdAdv51r0S15vcazvfPrByZ7GHggmU1Xlog4os0GwLeh2cXvmhHG3uFKoWf2AE; lmd_a_ld=cq%2FED61uukL7lcpak8TTaiZs9zIClG4B15G0HFJLvg0%3D; lmd_a_sp=2XZdAdv51r0S15vcazvfPrByZ7GHggmU1Xlog4os0GwLeh2cXvmhHG3uFKoWf2AE; lmd_stay_connected=0; lmd_a_m=SrWrUiyFGMNI4QIoA49%2FxiAOOuh06HZLaDsvqrJiujE%3D; euconsent-v2=CPdnuOJPdnuOJFzABCFRBdCgAAAAAAAAAAAAAAAAAAAA; lmd_consent=%7B%22userId%22%3A%228ce667c9-04da-4f5f-a51a-ca901765e8c2%22%2C%22timestamp%22%3A%221660307956.152987654%22%2C%22version%22%3A1%2C%22cmpId%22%3A371%2C%22displayMode%22%3A%22subscriber%22%2C%22purposes%22%3A%7B%22analytics%22%3Afalse%2C%22ads%22%3Afalse%2C%22personalization%22%3Afalse%2C%22mediaPlatforms%22%3Afalse%2C%22social%22%3Afalse%7D%7D; lmd_cap=_q7qieqqqk; lmd_a_c=1; lmd_ab=NWZpZin01OHmiqmF%2FPVOUHlBX%2FmLsfqwROGkFTQ51tC0LKUlQ9OBjeG0s7sFetkwLgwa%2BczdisIBS1em60MsSj774YBrng%3D%3D"
fileName = "Via_python.txt"

a_request = urllib.request.Request(urlToRetrieve)

a_request.add_header("Cookie", cookie)
with urllib.request.urlopen(a_request) as response:
   the_page = response.read()
   print(the_page)
   text_file = open(fileName, "wb")
   n = text_file.write(the_page)
   text_file.close()

# Retirer les balises "script"
import lxml.etree as le

with open('doc.xml','r') as f:
    doc=le.parse(f)
    for elem in doc.xpath('//*[attribute::lang]'):
        if elem.attrib['lang']=='en':
            elem.attrib.pop('lang')
        else:
            parent=elem.getparent()
            parent.remove(elem)
    print(le.tostring(doc))