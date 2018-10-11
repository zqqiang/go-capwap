import xml.etree.ElementTree as ET
from string import Template

tree = ET.parse('mgmt-data.xml')
root = tree.getroot()

fosVersion = '600'

platformSqlHeader = """
DROP TABLE IF EXISTS `wifi_platforms`;

CREATE TABLE `wifi_platforms` (
`oid` int(11) NOT NULL COMMENT 'platform oid',
`fosVersion` char(8) NOT NULL COMMENT 'fos version',
`captype` int(11) NOT NULL COMMENT 'platform.captype',
`platformName` char(6) DEFAULT NULL COMMENT 'platform.name',
`display` char(16) DEFAULT NULL COMMENT 'platform.help',
`wtpName` char(6) DEFAULT NULL COMMENT 'wtpcap.name',
`cap` int(11) NOT NULL COMMENT 'wtpcap.cap',
`maxVaps` int(11) NOT NULL COMMENT 'wtpcap.max_vaps',
`wanLan` int(11) NOT NULL COMMENT 'wtpcap.wan_lan',
`maxLan` int(11) NOT NULL COMMENT 'wtpcap.max_lan: max lan port number',
`bintMin` int(11) NOT NULL COMMENT 'wtpcap.bint_min: min beacon interval',
`bintMax` int(11) NOT NULL COMMENT 'wtpcap.bint_max: max beacon interval'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_platforms` WRITE;

INSERT INTO `wifi_platforms` VALUES 
"""

sqlFooter = """
UNLOCK TABLE;
"""


def buildPlatformRowSql(f, index, platform, wtpcap, last):
    platformLine = Template("$captype,'$name', '$help',").substitute(
        platform.attrib)
    wtpcapLine = Template(
        "'$name', $cap, $max_vaps, $wan_lan, $max_lan, $bint_min, $bint_max").substitute(wtpcap.attrib)
    f.write("(%d, '%s', %s %s)%s\n" %
            (index + 1, fosVersion, platformLine, wtpcapLine, ',' if not last else ';'))


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
                buildPlatformRowSql(f, i, platform, wtpcap,
                                    i == len(platforms) - 1)

    f.write(sqlFooter)


buildWifiPlatformSql()

bandSqlHeader = """
DROP TABLE IF EXISTS `wifi_bands`;

CREATE TABLE `wifi_bands` (
  `oid` int(11) NOT NULL COMMENT 'band oid',
  `fosVersion` char(8) NOT NULL COMMENT 'fos version',
  `name` char(16) DEFAULT NULL COMMENT 'band name',
  `help` char(16) DEFAULT NULL COMMENT 'band help',
  `bn` char(6) DEFAULT NULL COMMENT 'todo ?'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_bands` WRITE;

INSERT INTO `wifi_bands` VALUES 
"""


def buildBandRowSql(f, index, band, last):
    bandLine = Template("'$name', '$help', '$bn'").substitute(band.attrib)
    f.write("(%d, '%s', %s)%s\n" %
            (index + 1, fosVersion, bandLine, ',' if not last else ';'))


def buildWifiBandSql():
    bands = root.findall('.//wl_band_type/wlband')

    f = open('wifi_bands.sql', 'w')

    f.write(bandSqlHeader)

    for i, band in enumerate(bands):
        buildBandRowSql(f, i, band, i == len(bands) - 1)

    f.write(sqlFooter)


buildWifiBandSql()

radioSqlHeader = """
DROP TABLE IF EXISTS `wifi_radios`;

CREATE TABLE `wifi_radios` (
  `oid` int(11) NOT NULL COMMENT 'radio oid',
  `fosVersion` char(8) NOT NULL COMMENT 'fos version',
  `platformOid` int(11) NOT NULL COMMENT 'platform oid',
  `radioId` int(3) DEFAULT NULL COMMENT 'radio id',
  `maxMcs11n` int(8) DEFAULT NULL COMMENT '',
  `maxMcs11ac` int(8) DEFAULT NULL COMMENT '',
  `bandMask` char(64) DEFAULT NULL COMMENT '',
  `bandMaskGui` char(64) DEFAULT NULL COMMENT '',
  `bandDflt` char(64) DEFAULT NULL COMMENT '',
  `powMax2g` int(8) DEFAULT NULL COMMENT '',
  `powMax5g` int(8) DEFAULT NULL COMMENT '',
  `operMode` char(64) DEFAULT NULL COMMENT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_radios` WRITE;

INSERT INTO `wifi_radios` VALUES 
"""


def buildRadioRowSql(f, radioOid, platformOid, radio, last):
    radioLine = Template(
        "$id, $max_mcs_11n, $max_mcs_11ac, '$band_mask', '$band_mask_gui', '$band_dflt', $pow_max_2g, $pow_max_5g, '$oper_mode'").substitute(radio.attrib)
    f.write("(%d, '%s', %d, %s)%s\n" %
            (radioOid, fosVersion, platformOid, radioLine, ',' if not last else ';'))


def buildWifiRadiosSql():
    platforms = root.findall('.//cw_platform_type/platform')
    wtpcaps = root.findall('.//cw_wtp_cap/wtpcap')

    f = open('wifi_radios.sql', 'w')

    radioOid = 0

    f.write(radioSqlHeader)

    for i, platform in enumerate(platforms):
        for wtpcap in wtpcaps:
            if isCapTypeEqual(platform, wtpcap):
                radios = list(wtpcap.iter('radio'))
                for r, radio in enumerate(radios):
                    radioOid += 1
                    buildRadioRowSql(
                        f, radioOid, i + 1, radio, (i == len(platforms) - 1) and (r == len(radios) - 1))

    f.write(sqlFooter)


buildWifiRadiosSql()


channelSqlHeader = """
DROP TABLE IF EXISTS `wifi_channels`;

CREATE TABLE `wifi_channels` (
  `fosVersion` char(8) NOT NULL COMMENT 'fos version',
  `country` int(11) NOT NULL COMMENT 'country code',
  `band` int(11) NOT NULL COMMENT '',
  `bn` char(6) NOT NULL COMMENT 'bn',
  `bonding` char(6) NOT NULL COMMENT 'bonding: 20MHz, 40MHz, 80MHz',
  `outdoor` int(3) NOT NULL COMMENT 'outdoor: 0 disable, 1 enable',
  `channels` char(64) NOT NULL COMMENT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_channels` WRITE;

INSERT INTO `wifi_channels` VALUES 
"""


def buildWifiChannelRow(f, country, channel, last):
    if "bonding" in channel.attrib:
        channelLine = Template(
            "$band, '$bn', '$bonding', $outdoor").substitute(channel.attrib)
    else:
        channelLine = Template(
            "$band, '$bn', '', $outdoor").substitute(channel.attrib)

    f.write("('%s', %s, %s, '%s')%s\n" %
            (fosVersion, country.attrib["code"], channelLine, channel.text, ',' if not last else ';'))


def buildWifiChannelsSql():
    countries = root.findall('.//file[@name="wlchanlist.txt"]')
    country = countries[0]

    f = open('wifi_channels.sql', 'w')

    cf = open('chanlist.xml', 'w')
    cf.write(country.text.strip())

    ctree = ET.parse('chanlist.xml')
    croot = ctree.getroot()

    countries = croot.findall('.//country')
    channels = croot.findall('.//channel')

    f.write(channelSqlHeader)

    for cn, country in enumerate(countries):
        for ch, channel in enumerate(channels):
            buildWifiChannelRow(f, country, channel,
                                (cn == len(countries) - 1 and ch == len(channels) - 1))

    f.write(sqlFooter)


buildWifiChannelsSql()
