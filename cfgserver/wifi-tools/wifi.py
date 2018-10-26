import sys
import getopt
import os
import re
from os.path import join
from string import Template
import mysql.connector
import xml.etree.ElementTree as ET
from xml.parsers.expat import ExpatError, errors


countryNotForAp = [
    "511",     # Debug
    "0",       # No country set
    "124",     # Canada
    "392",     # Japan
    "412",     # South Korea
    "840",     # United States
    "393",     # Japan(JP1)
    "394",     # Japan(JP0)
    "395",     # Japan(JP1-1)
    "396",     # Japan(JE1)
    "397",     # Japan(JE2)
    "4006",    # Japan(JP6)
    "4007",    # Japan(J7)
    "4008",    # Japan(J8)
    "4009",    # Japan(J9)
    "4010",    # Japan(J10)
    "4011",    # Japan(J11)
    "4012",    # Japan(J12)
    "4013",    # Japan(J13)
    "4015",    # Japan(J15)
    "4016",    # Japan(J16)
    "4017",    # Japan(J17)
    "4018",    # Japan(J18)
    "4019",    # Japan(J19)
    "4020",    # Japan(J20)
    "4021",    # Japan(J21)
    "4022",    # Japan(J22)
    "4023",    # Japan(J23)
    "4024",    # Japan(J24)
    "4025",    # Japan(J25)
    "4026",    # Japan(J26)
    "4027",    # Japan(J27)
    "4028",    # Japan(J28)
    "4029",    # Japan(J29)
    "4030",    # Japan(J30)
    "4031",    # Japan(J31)
    "4032",    # Japan(J32)
    "4033",    # Japan(J33)
    "4034",    # Japan(J34)
    "4035",    # Japan(J35)
    "4036",    # Japan(J36)
    "4037",    # Japan(J37)
    "4038",    # Japan(J38)
    "4039",    # Japan(J39)
    "4040",    # Japan(J40)
    "4041",    # Japan(J41)
    "4042",    # Japan(J42)
    "4043",    # Japan(J43)
    "4044",    # Japan(J44)
    "4045",    # Japan(J45)
    "4046",    # Japan(J46)
    "4047",    # Japan(J47)
    "4048",    # Japan(J48)
    "4049",    # Japan(J49)
    "4050",    # Japan(J50)
    "4051",    # Japan(J51)
    "4052",    # Japan(J52)
    "4053",    # Japan(J53)
    "4054",    # Japan(J54)
    "4055",    # Japan(J55)
    "4056",    # Japan(J56)
    "4057",    # Japan(J57)
    "4058",    # Japan(J58)
    "4059",    # Japan(J59)
    "5000",    # Australia for AP only
    "5002"     # Belgium/Cisco implementation
]


def formatVersion(version):
    vl = []
    for c in version:
        vl.append(c)
    return "{0}.{1}.{2}".format(vl[0], vl[1], vl[2])


def isSameXmlDictionary(left, right):
    for k, v in left.items():
        v = v.rstrip('.')
        rv = right.attrib[k].rstrip('.')
        if not (rv == v):
            return False
    return True


def isSamePureDictionary(left, right):
    for k, v in left.items():
        if not (right[k] == v):
            return False
    return True


def isCountryForAp(countryCode):
    return countryCode not in countryNotForAp


sqlFooter = """;

UNLOCK TABLE;
"""

platformSqlHeader = """
DROP TABLE IF EXISTS `wifi_platforms`;

CREATE TABLE `wifi_platforms` (
`oid` int(11) NOT NULL COMMENT 'platform oid',
`platformName` char(6) DEFAULT NULL COMMENT 'platform.name',
`display` char(16) DEFAULT NULL COMMENT 'platform.help',
`snPrefix` char(16) DEFAULT NULL COMMENT 'serial number prefix',
`defaultProfileName` char(32) DEFAULT NULL COMMENT 'default profile name',
PRIMARY KEY (`oid`),
INDEX `platformName` (`platformName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_platforms` WRITE;

INSERT INTO `wifi_platforms` VALUES
"""


def buildPlatformRowSql(f, oid, platform, platforms, wtp, wtpProfile):
    platformLine = Template("'$name'").substitute(
        platform.attrib)
    help = platform.attrib['help'].rstrip('.')
    f.write("%s\n(%d, %s, '%s', '%s', '%s')" %
            ('' if 1 == platforms['oid'] else ',', oid, platformLine, help, wtp.attrib["name"], wtpProfile.attrib["name"]))

def getPlatformOid(platform, platforms):
    for oid, p in enumerate(platforms['rows']):
        if platform.attrib['name'] == p.attrib["name"]:
            if isSameXmlDictionary(p, platform):
                return oid + 1
    return 0


def buildWifiFosPlatformRow(f, fosVersion, platformOid, fosPlatforms):
    fosPlatforms['oid'] += 1
    f.write("%s\n('%s', %s)" %
            ('' if 1 == fosPlatforms['oid'] else ',', fosVersion, platformOid))


def buildWifiPlatformSql(root, version, platforms, fosPlatforms):
    p = root.findall('.//cw_platform_type/platform')
    
    if 0 == platforms['oid']:
        f = open('wifi_platforms.sql', 'w')
        f.write(platformSqlHeader)
        fo = open('wifi_fos_platforms.sql', 'w')
        fo.write(fosPlatformSqlHeader)
    else:
        f = open('wifi_platforms.sql', 'a')
        fo = open('wifi_fos_platforms.sql', 'a')

    for i, platform in enumerate(p):
        oid = getPlatformOid(platform, platforms)
        if 0 == oid:
            platforms['oid'] += 1
            platforms['rows'].append(platform)
            oid = platforms['oid']
            wtp = root.find('.//cw_wtp_name/wtp[@captype="{0}"]'.format(platform.attrib["captype"]))
            wtpProfile = root.find(
                './/cw_wtpprof_name/wtpprof[@captype="{0}"]'.format(platform.attrib["captype"]))
            buildPlatformRowSql(f, oid, platform, platforms, wtp, wtpProfile)
        buildWifiFosPlatformRow(fo, formatVersion(version), oid, fosPlatforms)


def getRadioOid(radio, radios):
    for oid, r in enumerate(radios['rows']):
        if isSameXmlDictionary(r, radio):
            return oid + 1
    return 0


def getRadioKeyOid(version, name, radioKey):
    for oid, rk in enumerate(radioKey['rows']):
        if isSamePureDictionary(rk, {'fosVersion': version, 'name': name}):
            return oid + 1
    return 0


def getDefaultBand(defaultBand, bands):
    for b, band in enumerate(bands):
        if band.attrib["bn"] == defaultBand:
            return b + 1


def buildRadioRowSql(f, oid, radio, radios, bands):
    radioLine = Template(
        "$id, $max_mcs_11n, $max_mcs_11ac, $pow_max_2g, $pow_max_5g").substitute(radio.attrib)
    defaultBand = getDefaultBand(radio.attrib['band_dflt'], bands)
    f.write("%s\n(%d, %s, %s)" %
            ('' if 1 == radios['oid'] else ',', oid, radioLine, defaultBand))


def buildRadioKeyRowSql(f, koid, version, name, radioKey):
    f.write("%s\n(%d, '%s', '%s')" %
            ('' if 1 == radioKey['oid'] else ',', koid, version, name))


def buildRadioMapRowSql(f, koid, oid, radioMap):
    f.write("%s\n(%d, %d)" %
            ('' if 1 == radioMap['oid'] else ',', koid, oid))


def buildWifiRadioSql(root, version, radios, radioKey, radioMap, radioBand, bands):
    wtpcaps = root.findall('.//cw_wtp_cap/wtpcap')
    for w in wtpcaps:
        name = w.attrib["name"]
        rs = list(w.iter('radio'))
        for r in rs:
            if 0 == radios["oid"]:
                rf = open('wifi_radios.sql', 'w')
                rf.write(radioSqlHeader)
            else:
                rf = open('wifi_radios.sql', 'a')

            if 0 == radioKey['oid']:
                rk = open('wifi_radio_key.sql', 'w')
                rk.write(radioKeySqlHeader)
            else:
                rk = open('wifi_radio_key.sql', 'a')

            if 0 == radioMap['oid']:
                rm = open('wifi_radio_map.sql', 'w')
                rm.write(radioMapSqlHeader)
            else:
                rm = open('wifi_radio_map.sql', 'a')

            if 0 == radioBand['oid']:
                rb = open('wifi_radio_band.sql', 'w')
                rb.write(radioBandSqlHeader)
            else:
                rb = open('wifi_radio_band.sql', 'a')

            oid = getRadioOid(r, radios)
            if 0 == oid:
                radios["oid"] += 1
                radios["rows"].append(r)
                oid = radios['oid']
                buildRadioRowSql(rf, oid, r, radios, bands)
                buildRadioBandRowSql(rb, oid, r, bands, radioBand)

            koid = getRadioKeyOid(version, name, radioKey)
            if 0 == koid:
                radioKey['oid'] += 1
                radioKey['rows'].append(
                    {'fosVersion': version, 'name': name})
                koid = radioKey['oid']
                buildRadioKeyRowSql(rk, koid, formatVersion(
                    version), name, radioKey)

            radioMap['oid'] += 1
            # print("fos version: {0}, wtp: {1}, key oid: {2}, radio oid: {3}".format(
                # version, w.attrib, koid, oid))
            buildRadioMapRowSql(rm, koid, oid, radioMap)


fosPlatformSqlHeader = """
DROP TABLE IF EXISTS `wifi_fos_platforms`;

CREATE TABLE `wifi_fos_platforms` (
`fosVersion` char(8) NOT NULL COMMENT 'fos version',
`platformOid` int(11) NOT NULL COMMENT 'platform oid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_fos_platforms` WRITE;

INSERT INTO `wifi_fos_platforms` VALUES
"""


bandSqlHeader = """
DROP TABLE IF EXISTS `wifi_bands`;

CREATE TABLE `wifi_bands` (
  `oid` int(11) NOT NULL COMMENT 'band oid',
  `name` char(16) DEFAULT NULL COMMENT 'band name',
  `help` char(32) DEFAULT NULL COMMENT 'band help',
  `bn` char(6) DEFAULT NULL COMMENT 'todo ?',
  `frequency` char(6) DEFAULT NULL COMMENT 'band frequency',
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_bands` WRITE;

INSERT INTO `wifi_bands` VALUES
"""

freqMap = ['5', '2.4', '2.4', '2.4', '5',
           '5', '2.4', '2.4', '2.4', '5', '5', '5']


def buildBandRowSql(f, oid, band):
    bandLine = Template("'$name', '$help', '$bn'").substitute(band.attrib)
    f.write("%s\n(%d, %s, %s)" %
            ('' if 1 == oid else ',', oid, bandLine, freqMap[oid - 1]))


def buildWifiBandSql(root):
    bands = root.findall('.//wl_band_type/wlband')

    f = open("wifi_bands.sql", 'w')

    f.write(bandSqlHeader)

    for i, band in enumerate(bands):
        buildBandRowSql(f, i + 1, band)

    f.write(sqlFooter)

    return bands


radioSqlHeader = """
DROP TABLE IF EXISTS `wifi_radios`;

CREATE TABLE `wifi_radios` (
  `oid` int(11) NOT NULL COMMENT 'radio oid',
  `radioId` int(3) DEFAULT NULL COMMENT 'radio id',
  `maxMcs11n` int(8) DEFAULT NULL COMMENT '',
  `maxMcs11ac` int(8) DEFAULT NULL COMMENT '',
  `powMax2g` int(8) DEFAULT NULL COMMENT 'band 2g, auto tx power, tx power max dBm',
  `powMax5g` int(8) DEFAULT NULL COMMENT 'band 5g, auto tx power, tx power max dBm',
  `defaultBandOid` int(11) DEFAULT NULL COMMENT 'default band oid',
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_radios` WRITE;

INSERT INTO `wifi_radios` VALUES
"""

radioKeySqlHeader = """
DROP TABLE IF EXISTS `wifi_radio_key`;

CREATE TABLE `wifi_radio_key` (
  `oid` int(11) NOT NULL COMMENT 'radio key oid',
  `fosVersion` char(8) NOT NULL COMMENT 'fos version',
  `apPlatformName` char(6) NOT NULL COMMENT 'ap platform name',
  PRIMARY KEY (`oid`),
  INDEX `fosVersion` (`fosVersion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_radio_key` WRITE;

INSERT INTO `wifi_radio_key` VALUES
"""

radioMapSqlHeader = """
DROP TABLE IF EXISTS `wifi_radio_map`;

CREATE TABLE `wifi_radio_map` (
  `radioKeyOid` int(11) NOT NULL COMMENT 'radio key oid',
  `radioOid` int(11) NOT NULL COMMENT 'radio oid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_radio_map` WRITE;

INSERT INTO `wifi_radio_map` VALUES
"""


radioBandSqlHeader = """
DROP TABLE IF EXISTS `wifi_radio_band`;

CREATE TABLE `wifi_radio_band` (
  `radioOid` int(3) DEFAULT NULL COMMENT 'radio oid',
  `bandOid` int(11) NOT NULL COMMENT 'band oid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_radio_band` WRITE;

INSERT INTO `wifi_radio_band` VALUES
"""


def isInBandMask(bn, mask):
    maskList = mask.split(' ')
    return bn in maskList


def buildRadioBandRowSql(f, radioOid, radio, bands, radioBand):
    for bandOid, b in enumerate(bands):
        if isInBandMask(b.attrib['bn'], radio.attrib['band_mask']):
            radioBand['oid'] += 1
            f.write("%s\n(%s, %s)" %
                    ('' if 1 == radioBand['oid'] else ',', radioOid, bandOid + 1))


def isBandEqual(radio, band):
    mask = radio.attrib["band_mask"].split(' ')
    bn = band.attrib["bn"]
    return bn in mask


channelKeySqlHeader = """
DROP TABLE IF EXISTS `wifi_channel_key`;

CREATE TABLE `wifi_channel_key` (
  `oid` int(11) NOT NULL COMMENT 'key oid',
  `fosVersion` char(8) NOT NULL COMMENT 'fos version',
  `countryIso` char(8) NOT NULL COMMENT 'country iso',
  `band` int(11) NOT NULL COMMENT '',
  `bn` char(6) NOT NULL COMMENT 'bn',
  `bonding` char(6) NOT NULL COMMENT 'bonding: none, all plus, minus, 80MHz',
  `outdoor` int(3) NOT NULL COMMENT 'outdoor: 0 disable, 1 enable',
  PRIMARY KEY(`oid`),
  INDEX `fosVersion` (`fosVersion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_channel_key` WRITE;

INSERT INTO `wifi_channel_key` VALUES
"""

channelMapSqlHeader = """
DROP TABLE IF EXISTS `wifi_channel_map`;

CREATE TABLE `wifi_channel_map` (
  `channelKeyOid` int(11) NOT NULL COMMENT 'channel key oid',
  `channelNumber` int(8) NOT NULL COMMENT 'channel number',
  INDEX `channelKeyOid` (`channelKeyOid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_channel_map` WRITE;

INSERT INTO `wifi_channel_map` VALUES
"""

countrySqlHeader = """
DROP TABLE IF EXISTS `wifi_countries`;

CREATE TABLE `wifi_countries` (
  `oid` int(11) NOT NULL COMMENT 'country oid',
  `iso` char(8) NOT NULL COMMENT 'country iso name',
  `code` int(11) NOT NULL COMMENT 'country code',
  `dmn` int(11) NOT NULL COMMENT 'country dmn ?',
  `name` char(64) NOT NULL COMMENT 'country name',
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_countries` WRITE;

INSERT INTO `wifi_countries` VALUES
"""


def getCountryOid(country, countries):
    for oid, c in enumerate(countries['rows']):
        if country.attrib['iso'] == c.attrib["iso"]:
            if isSameXmlDictionary(c, country):
                return oid + 1
    return 0


def buildWifiCountryRow(f, countryOid, country):
    countryLine = Template(
        "'$iso', $code, $dmn").substitute(country.attrib)
    countryName = country.attrib['name'].title().rstrip('2')
    f.write("%s\n(%d, %s, '%s')" %
            ('' if (1 == countryOid) else ',', countryOid, countryLine, countryName))


fosCountrySqlHeader = """
DROP TABLE IF EXISTS `wifi_fos_countries`;

CREATE TABLE `wifi_fos_countries` (
  `fosVersion` char(8) NOT NULL COMMENT 'fos version',
  `countryOid` int(11) NOT NULL COMMENT 'country oid',
  INDEX `fosVersion` (`fosVersion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_fos_countries` WRITE;

INSERT INTO `wifi_fos_countries` VALUES
"""


def buildWifiFosCountryRow(f, fosVersion, countryOid, fosCountries):
    fosCountries['oid'] += 1
    f.write("%s\n('%s', %s)" %
            ('' if 1 == fosCountries['oid'] else ',', fosVersion, countryOid))


def buildChannelKeyRow(f, fosVersion, countryIso, channel, channelKey):
    channelKey['oid'] += 1
    if "bonding" in channel.attrib:
        channelLine = Template(
            "$band, '$bn', '$bonding', $outdoor").substitute(channel.attrib)
    else:
        channelLine = Template(
            "$band, '$bn', 'none', $outdoor").substitute(channel.attrib)
    f.write("%s\n(%s,'%s','%s',%s)" % (
        '' if 1 == channelKey['oid'] else ',', channelKey['oid'], fosVersion, countryIso, channelLine))

def isNoAccess(countryIso, channelNumber):
    if countryIso in ['US', 'CA', 'PS']:
        if channelNumber in ['120', '124', '128']:
            return True
    return False


def buildChannelMapRow(f, channelKeyOid, channel, channelMap, countryIso):
    if channel.text != None:
        channels = channel.text
    else:
        channels = ''

    clist = channels.split(',')
    for cv in clist:
        channelNumber = re.sub('[\+\-\*]', '', cv)
        if channelNumber and not isNoAccess(countryIso, channelNumber):
            channelMap['oid'] += 1
            f.write("%s\n(%d, '%s')" %
                    ('' if 1 == channelMap['oid'] else ',', channelKeyOid, cv))


def buildWifiCountryAndChannelSql(croot, version, countries, fosCountries, channelKey, channelMap):
    cs = croot.findall('.//country')

    if 0 == countries['oid']:
        f = open('wifi_countries.sql', 'w')
        f.write(countrySqlHeader)
        fo = open('wifi_fos_countries.sql', 'w')
        fo.write(fosCountrySqlHeader)
    else:
        f = open('wifi_countries.sql', 'a')
        fo = open('wifi_fos_countries.sql', 'a')

    if 0 == channelKey['oid']:
        fck = open('wifi_channel_key.sql', 'w')
        fck.write(channelKeySqlHeader)
    else:
        fck = open('wifi_channel_key.sql', 'a')

    if 0 == channelMap['oid']:
        fcm = open('wifi_channel_map.sql', 'w')
        fcm.write(channelMapSqlHeader)
    else:
        fcm = open('wifi_channel_map.sql', 'a')

    for country in cs:
        if isCountryForAp(country.attrib['code']):
            countryOid = getCountryOid(country, countries)
            if 0 == countryOid:
                countries['oid'] += 1
                countries['rows'].append(country)
                countryOid = countries['oid']
                buildWifiCountryRow(f, countryOid, country)
            buildWifiFosCountryRow(
                fo, formatVersion(version), countryOid, fosCountries)
            chs = list(country.iter('channel'))
            countryIso = country.attrib["iso"]
            for c in chs:
                buildChannelKeyRow(fck, formatVersion(
                    version), countryIso, c, channelKey)
                buildChannelMapRow(
                    fcm, channelKey['oid'], c, channelMap, country.attrib['iso'])


def runSql(host, username, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=username,
        passwd=password,
        database=database
    )
    cursor = conn.cursor()

    scripts = []

    for folder, dirs, files in os.walk("."):
        if "." == folder:
            for f in files:
                if ".sql" in f:
                    scripts.append(f)

    for script in scripts:
        f = open(script, "r")
        sql = f.read()
        cmds = sql.replace("\n", "").split(";")

        for cmd in cmds:
            cursor.execute(cmd)

    conn.close()


def extractChanListXml(root, version):
    countries = root.findall('.//file[@name="wlchanlist.txt"]')
    country = countries[0]

    f = open('chanlist_{0}.xml'.format(version), 'w')
    f.write(country.text.strip())

    tree = ET.parse('chanlist_{0}.xml'.format(version))
    croot = tree.getroot()
    return croot


viewSql = """
CREATE OR REPLACE VIEW `wifi_fos_platform_radio_band` AS 
SELECT fosVersion, platformName, rm.radioOid, radioid, bandOid
    FROM wifi_radio_band rb
    INNER JOIN wifi_radio_map rm ON rm.radioOid = rb.radioOid
    INNER JOIN wifi_radio_key rk ON rk.oid = rm.radioKeyOid
    INNER JOIN wifi_platforms p ON p.platformName = rk.apPlatformName
    INNER JOIN wifi_radios r ON r.oid = rm.radioOid;
"""


def buildView():
    f = open('wifi_view.sql', 'w')
    f.write(viewSql)

dfsSql = """
DROP TABLE IF EXISTS `wifi_dfs`;

CREATE TABLE `wifi_dfs` (
  `fosVersion` char(8) NOT NULL COMMENT 'fos version',
  `countryIso` char(8) NOT NULL COMMENT 'country iso',
  `snPrefix` char(8) NOT NULL COMMENT 'ap sn prefix',
  INDEX `versionIsoPrefixIndex` (`fosVersion`,`countryIso`,`snPrefix`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_dfs` WRITE;

INSERT INTO `wifi_dfs` VALUES
"""

def buildDfsMap():
    cfile = open("wlchanlist.c", 'r')
    start = False
    osVersion = 0
    mrVersion = 0
    dfsOid = 0

    sfile = open('wifi_dfs.sql', 'w')
    sfile.write(dfsSql)

    for line in cfile.readlines():
        if not start:
            if "static const FTNT_REGCODE_MAPPING ftntRegcodePairs" in line:
                start = True
        elif start and "};" in line:
            start = False
        else:
            if '[DVM_OS_VER_5] = {' in line:
                osVersion = 5
            elif '[DVM_OS_VER_6] = {' in line:
                osVersion = 6
            elif '[0] = {' in line:
                mrVersion = 0
            elif '[2] = {' in line:
                mrVersion = 2
            elif '[4] = {' in line:
                mrVersion = 4
            elif '[6] = {' in line:
                mrVersion = 6
            else:
                row = line.strip()
                if row.startswith('/*') or '{ NULL },' == row or '},' == row:
                    continue
                row = row.lstrip('{')
                row = row.rstrip('},')
                rowList = row.split(',')
                countryIso = rowList[2].strip().strip('"')
                dfs = rowList[3].strip()
                platforms = rowList[4].strip().strip('"').split(" ")
                if dfs == '1':
                    for platform in platforms:
                        dfsOid += 1
                        sfile.write("%s\n('%s.%s.0', '%s','%s')" % ('' if dfsOid == 1 else ',', osVersion, mrVersion, countryIso, platform))


def run():
    path = "D:\\Workspaces\\svn\\fos_mgmt_data"
    bands = None
    countries = {'oid': 0, 'rows': []}
    fosCountries = {'oid': 0}

    platforms = {'oid': 0, 'rows': []}
    fosPlatforms = {'oid': 0}

    radios = {'oid': 0, 'rows': []}
    radioKey = {'oid': 0, 'rows': []}
    radioMap = {'oid': 0}
    radioBand = {'oid': 0}

    channelKey = {'oid': 0}
    channelMap = {'oid': 0}

    for folder, dirs, files in os.walk(path):
        if '.svn' in folder:
            continue
        if not dirs and files:
            version = folder.split('\\')[-1]
            for f in files:
                fxml = "FortiGate-60D-{0}".format(version)
                if fxml not in f:
                    continue
                # print("xml file: {0}".format(f))
                tree = ET.parse(join(folder, f))
                root = tree.getroot()

                if not bands:
                    bands = buildWifiBandSql(root)

                croot = extractChanListXml(root, version)
                buildWifiCountryAndChannelSql(
                    croot, version, countries, fosCountries, channelKey, channelMap)
                buildWifiPlatformSql(root, version, platforms, fosPlatforms)
                buildWifiRadioSql(root, version, radios,
                                  radioKey, radioMap, radioBand, bands)

    buildDfsMap()

    for folder, dirs, files in os.walk("."):
        if "." == folder:
            for f in files:
                if ".sql" in f:
                    fs = open(f, 'a')
                    fs.write(sqlFooter)

    buildView()


def usage():
    print('wifi.py -h <host> -u <username> -p <password> -d <database>')


def setup():
    for folder, dirs, files in os.walk("."):
        if "." == folder:
            for f in files:
                if ".sql" in f:
                    os.remove(f)
                    print("remove {0}".format(f))


def cleanup():
    for folder, dirs, files in os.walk("."):
        if "." == folder:
            for f in files:
                if ".xml" in f:
                    os.remove(f)
                    print("remove {0}".format(f))


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:u:p:d:", [
            "host=", "username=", "password=", "database="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    host = ""
    username = ""
    password = ""
    database = ""

    for opt, arg in opts:
        if opt in ("-h", "--host"):
            host = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-d", "--database"):
            database = arg

    setup()

    run()

    cleanup()

    runSql(host, username, password, database)


if __name__ == "__main__":
    main()
