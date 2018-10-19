import sys
import getopt
import os
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
        if not (right.attrib[k] == v):
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
`captype` int(11) NOT NULL COMMENT 'platform.captype',
`platformName` char(6) DEFAULT NULL COMMENT 'platform.name',
`display` char(16) DEFAULT NULL COMMENT 'platform.help',
PRIMARY KEY (`oid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_platforms` WRITE;

INSERT INTO `wifi_platforms` VALUES
"""


def buildPlatformRowSql(f, oid, platform, platforms):
    platformLine = Template("$captype,'$name'").substitute(
        platform.attrib)
    help = platform.attrib['help'].rstrip('.')
    f.write("%s\n(%d, %s, '%s')" %
            ('' if 1 == platforms['oid'] else ',', oid, platformLine, help))


def isCapTypeEqual(platform, wtpcap):
    return wtpcap.attrib['captype'] == platform.attrib['captype']


def getPlatformOid(platform, platforms):
    for oid, p in enumerate(platforms['rows']):
        if platform.attrib['captype'] == p.attrib["captype"]:
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
            buildPlatformRowSql(f, oid, platform, platforms)
        buildWifiFosPlatformRow(fo, formatVersion(version), oid, fosPlatforms)


def getRadioOid(radio, radios):
    for oid, r in enumerate(radios['rows']):
        if isSameXmlDictionary(r, radio):
            return oid + 1
    return 0


def getRadioKeyOid(version, capType, radioKey):
    for oid, rk in enumerate(radioKey['rows']):
        if isSamePureDictionary(rk, {'fosVersion': version, 'capType': capType}):
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


def buildRadioKeyRowSql(f, koid, version, capType, radioKey):
    f.write("%s\n(%d, '%s', '%s')" %
            ('' if 1 == radioKey['oid'] else ',', koid, version, capType))


def buildRadioMapRowSql(f, koid, oid, radioMap):
    f.write("%s\n(%d, %d)" %
            ('' if 1 == radioMap['oid'] else ',', koid, oid))


def buildWifiRadioSql(root, version, radios, radioKey, radioMap, radioBand, bands):
    wtpcaps = root.findall('.//cw_wtp_cap/wtpcap')
    for w in wtpcaps:
        capType = w.attrib["captype"]
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

            koid = getRadioKeyOid(version, capType, radioKey)
            if 0 == koid:
                radioKey['oid'] += 1
                radioKey['rows'].append(
                    {'fosVersion': version, 'capType': capType})
                koid = radioKey['oid']
                buildRadioKeyRowSql(rk, koid, formatVersion(
                    version), capType, radioKey)

            radioMap['oid'] += 1
            buildRadioMapRowSql(rm, koid, oid, radioMap)

            buildRadioBandRowSql(rb, oid, r, bands, radioBand)


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
  `capType` int(11) NOT NULL COMMENT 'platform captype',
  PRIMARY KEY (`oid`)
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


def buildRadioBandRowSql(f, radioOid, radio, bands, radioBand):
    for bandOid, b in enumerate(bands):
        if b.attrib['bn'] in radio.attrib['band_mask']:
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
  `country` int(11) NOT NULL COMMENT 'country code',
  `band` int(11) NOT NULL COMMENT '',
  `bn` char(6) NOT NULL COMMENT 'bn',
  `bonding` char(6) NOT NULL COMMENT 'bonding: none, all plus, minus, 80MHz',
  `outdoor` int(3) NOT NULL COMMENT 'outdoor: 0 disable, 1 enable',
  PRIMARY KEY(`oid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_channel_key` WRITE;

INSERT INTO `wifi_channel_key` VALUES
"""

channelMapSqlHeader = """
DROP TABLE IF EXISTS `wifi_channel_map`;

CREATE TABLE `wifi_channel_map` (
  `oid` int(11) NOT NULL COMMENT 'channel key oid',
  `channel` char(8) NOT NULL COMMENT 'channel value'
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
    countryName = country.attrib['name'].title()
    f.write("%s\n(%d, %s, '%s')" %
            ('' if (1 == countryOid) else ',', countryOid, countryLine, countryName))


fosCountrySqlHeader = """
DROP TABLE IF EXISTS `wifi_fos_countries`;

CREATE TABLE `wifi_fos_countries` (
  `fosVersion` char(8) NOT NULL COMMENT 'fos version',
  `countryOid` int(11) NOT NULL COMMENT 'country oid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_fos_countries` WRITE;

INSERT INTO `wifi_fos_countries` VALUES
"""


def buildWifiFosCountryRow(f, fosVersion, countryOid, fosCountries):
    fosCountries['oid'] += 1
    f.write("%s\n('%s', %s)" %
            ('' if 1 == fosCountries['oid'] else ',', fosVersion, countryOid))


def buildChannelKeyRow(f, fosVersion, countryOid, channel, channelKey):
    channelKey['oid'] += 1
    if "bonding" in channel.attrib:
        channelLine = Template(
            "$band, '$bn', '$bonding', $outdoor").substitute(channel.attrib)
    else:
        channelLine = Template(
            "$band, '$bn', 'none', $outdoor").substitute(channel.attrib)
    f.write("%s\n(%s,'%s',%s,%s)" % (
        '' if 1 == channelKey['oid'] else ',', channelKey['oid'], fosVersion, countryOid, channelLine))


def buildChannelMapRow(f, channelKeyOid, channel, channelMap):
    if channel.text != None:
        channels = channel.text
    else:
        channels = ''

    clist = channels.split(',')
    for cv in clist:
        if cv:
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
            for c in chs:
                buildChannelKeyRow(fck, formatVersion(
                    version), countryOid, c, channelKey)
                buildChannelMapRow(fcm, channelKey['oid'], c, channelMap)


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
    SELECT fosVersion, platformName, rb.radioOid, bandOid
    FROM wifi_radio_band rb
        INNER JOIN wifi_radio_map rm ON rm.radioOid = rb.radioOid
        INNER JOIN wifi_radio_key rk ON rk.oid = rm.radioKeyOid
        INNER JOIN wifi_platforms p ON p.capType = rk.capType;
"""


def buildView():
    f = open('wifi_view.sql', 'w')
    f.write(viewSql)


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
            tree = ET.parse(join(folder, files[0]))
            root = tree.getroot()

            if not bands:
                bands = buildWifiBandSql(root)

            croot = extractChanListXml(root, version)
            buildWifiCountryAndChannelSql(
                croot, version, countries, fosCountries, channelKey, channelMap)
            buildWifiPlatformSql(root, version, platforms, fosPlatforms)
            buildWifiRadioSql(root, version, radios,
                              radioKey, radioMap, radioBand, bands)

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
