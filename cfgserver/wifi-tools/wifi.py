import xml.etree.ElementTree as ET

tree = ET.parse('mgmt-data.xml')
root = tree.getroot()

platforms = root.findall('.//cw_platform_type/platform')

for platform in platforms:
    print(platform.tag, platform.attrib)

wtpcaps = root.findall('.//cw_wtp_cap/wtpcap')

for wtpcap in wtpcaps:
    print(wtpcap.tag, wtpcap.attrib)
    radios = wtpcap.findall('radio')
    for radio in radios:
        print(radio.tag, radio.attrib)
