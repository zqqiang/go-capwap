import xml.etree.ElementTree as ET
from string import Template

tree = ET.parse('mgmt-data.xml')
root = tree.getroot()

platformSqlHeader = """
DROP TABLE IF EXISTS 'wifi_platforms';

CREATE TABLE 'wifi_platforms' (
'oid' int(11) NOT NULL COMMENT 'platform oid',
'captype' int(11) NOT NULL COMMENT 'platform.captype',
'platformName' char(6) DEFAULT NULL COMMENT 'platform.name',
'display' char(16) DEFAULT NULL COMMENT 'platform.help',
'wtpName' char(6) DEFAULT NULL COMMENT 'wtpcap.name',
'cap' int(11) NOT NULL COMMENT 'wtpcap.cap',
'maxVaps' int(11) NOT NULL COMMENT 'wtpcap.max_vaps',
'wanLan' int(11) NOT NULL COMMENT 'wtpcap.wan_lan',
'maxLan' int(11) NOT NULL COMMENT 'wtpcap.max_lan: max lan port number',
'bintMin' int(11) NOT NULL COMMENT 'wtpcap.bint_min: min beacon interval',
'bintMax' int(11) NOT NULL COMMENT 'wtpcap.bint_max: max beacon interval'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES 'wifi_platforms' WRITE;

INSERT INTO 'wifi_platforms' VALUES 
"""

platformSqlFooter = """
UNLOCK TABLE;
"""


def buildPlatformRowSql(f, index, platform, wtpcap):
    platformLine = Template("$captype,'$name', '$help',").substitute(
        platform.attrib)
    wtpcapLine = Template(
        "'$name', $cap, $max_vaps, $wan_lan, $max_lan, $bint_min, $bint_max").substitute(wtpcap.attrib)
    f.write("   (%d, %s %s),\n" %
            (index + 1, platformLine, wtpcapLine))


def isCapTypeEqual(platform, wtpcap):
    return wtpcap.attrib['captype'] == platform.attrib['captype']


def buildWifiPlatformSql():
    platforms = root.findall('.//cw_platform_type/platform')
    wtpcaps = root.findall('.//cw_wtp_cap/wtpcap')

    f = open('wifi_platforms.sql', 'w')

    f.write(platformSqlHeader)

    for i, platform in enumerate(platforms):
        for wtpcap in wtpcaps:
            if isCapTypeEqual(platform, wtpcap):
                buildPlatformRowSql(f, i, platform, wtpcap)

    f.write(platformSqlFooter)


buildWifiPlatformSql()
