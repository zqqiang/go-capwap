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


def isSameDictionary(left, right):
    for k, v in left.items():
        if not (right.attrib[k] == v):
            return False
    return True


def isCountryForAp(countryCode):
    return countryCode not in countryNotForAp


sqlFooter = """;

UNLOCK TABLE;
"""

# `cap` int(11) NOT NULL COMMENT 'wtpcap.cap',
# `maxVaps` int(11) NOT NULL COMMENT 'wtpcap.max_vaps',
# `wanLan` int(11) NOT NULL COMMENT 'wtpcap.wan_lan',
# `maxLan` int(11) NOT NULL COMMENT 'wtpcap.max_lan: max lan port number',
# `bintMin` int(11) NOT NULL COMMENT 'wtpcap.bint_min: min beacon interval',
# `bintMax` int(11) NOT NULL COMMENT 'wtpcap.bint_max: max beacon interval',

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
            if isSameDictionary(p, platform):
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
        if isSameDictionary(r, radio):
            return oid + 1
    return 0


def buildRadioRowSql(f, oid, radio, radios):
    radioLine = Template(
        "$id, $max_mcs_11n, $max_mcs_11ac, $pow_max_2g, $pow_max_5g").substitute(radio.attrib)
    f.write("%s\n(%d, %s)" %
            ('' if 1 == radios['oid'] else ',', oid, radioLine))


def buildWifiRadioSql(root, version, radios, radioKey, radioMap):
    wtpcaps = root.findall('.//cw_wtp_cap/wtpcap')
    for w in wtpcaps:
        captype = w.attrib["captype"]
        rs = list(w.iter('radio'))
        for r in rs:
            radioId = r.attrib['id']

            if 0 == radios["oid"]:
                rf = open('wifi_radios.sql', 'w')
                rf.write(radioSqlHeader)
            else:
                rf = open('wifi_radios.sql', 'a')

            oid = getRadioOid(r, radios)
            if 0 == oid:
                radios["oid"] += 1
                radios["rows"].append(r)
                oid = radios['oid']
                buildRadioRowSql(rf, oid, r, radios)

    # if 0 == platforms['oid']:
    #     f = open('wifi_platforms.sql', 'w')
    #     f.write(platformSqlHeader)
    #     fo = open('wifi_fos_platforms.sql', 'w')
    #     fo.write(fosPlatformSqlHeader)
    # else:
    #     f = open('wifi_platforms.sql', 'a')
    #     fo = open('wifi_fos_platforms.sql', 'a')

    # for i, platform in enumerate(p):
    #     oid = getPlatformOid(platform, platforms)
    #     if 0 == oid:
    #         platforms['oid'] += 1
    #         platforms['rows'].append(platform)
    #         oid = platforms['oid']
    #         buildPlatformRowSql(f, oid, platform, platforms)
    #     buildWifiFosPlatformRow(fo, formatVersion(version), oid, fosPlatforms)


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
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_bands` WRITE;

INSERT INTO `wifi_bands` VALUES
"""


def buildBandRowSql(f, index, band):
    bandLine = Template("'$name', '$help', '$bn'").substitute(band.attrib)
    f.write("%s\n(%d, %s)" %
            ('' if 1 == index else ',', index, bandLine))


def buildWifiBandSql(root):
    bands = root.findall('.//wl_band_type/wlband')

    f = open("wifi_bands.sql", 'w')

    f.write(bandSqlHeader)

    for i, band in enumerate(bands):
        buildBandRowSql(f, i + 1, band)

    f.write(sqlFooter)

    return bands

#   `operMode` char(64) DEFAULT NULL COMMENT 'disable: Disabled, fg: Dedicated Monitor, ap: Access Point, apbg2: ?',
#   `bandDflt` char(64) DEFAULT NULL COMMENT '',


radioSqlHeader = """
DROP TABLE IF EXISTS `wifi_radios`;

CREATE TABLE `wifi_radios` (
  `oid` int(11) NOT NULL COMMENT 'radio oid',
  `radioId` int(3) DEFAULT NULL COMMENT 'radio id',
  `maxMcs11n` int(8) DEFAULT NULL COMMENT '',
  `maxMcs11ac` int(8) DEFAULT NULL COMMENT '',
  `powMax2g` int(8) DEFAULT NULL COMMENT 'band 2g, auto tx power, tx power max dBm',
  `powMax5g` int(8) DEFAULT NULL COMMENT 'band 5g, auto tx power, tx power max dBm',
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_radios` WRITE;

INSERT INTO `wifi_radios` VALUES
"""


# def getDefaultBand(defaultBand):
#     bands = root.findall('.//wl_band_type/wlband')
#     for b, band in enumerate(bands):
#         if band.attrib["bn"] == defaultBand:
#             return b + 1


# def buildRadioRowSql(f, capType, radio, last):
#     radioLine = Template(
#         "$id, $max_mcs_11n, $max_mcs_11ac, $pow_max_2g, $pow_max_5g, '$oper_mode'").substitute(radio.attrib)
#     f.write("(%s, %s, %s)%s\n" %
#             (capType, radioLine, getDefaultBand(radio.attrib["band_dflt"]), ',' if not last else ';'))


# def buildWifiRadiosSql():
#     platforms = root.findall('.//cw_platform_type/platform')
#     wtpcaps = root.findall('.//cw_wtp_cap/wtpcap')

#     f = open('wifi_radios.sql', 'w')

#     f.write(radioSqlHeader)

#     for i, platform in enumerate(platforms):
#         for wtpcap in wtpcaps:
#             if isCapTypeEqual(platform, wtpcap):
#                 radios = list(wtpcap.iter('radio'))
#                 for r, radio in enumerate(radios):
#                     buildRadioRowSql(f, platform.attrib["captype"], radio, (i == len(
#                         platforms) - 1) and (r == len(radios) - 1))

#     f.write(sqlFooter)


radioBandSqlHeader = """
DROP TABLE IF EXISTS `wifi_radio_band`;

CREATE TABLE `wifi_radio_band` (
  `capType` int(11) NOT NULL COMMENT 'platform captype',
  `radioId` int(3) DEFAULT NULL COMMENT 'radio id',
  `bandOid` int(11) NOT NULL COMMENT 'band oid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_radio_band` WRITE;

INSERT INTO `wifi_radio_band` VALUES
"""


def buildRadioBandRowSql(f, capType, radioId, bandOid, last):
    f.write("(%s, %s, %s)%s\n" %
            (capType, radioId, bandOid, ',' if not last else ';'))


def isBandEqual(radio, band):
    mask = radio.attrib["band_mask"].split(' ')
    bn = band.attrib["bn"]
    return bn in mask


def buildWifiRadioBandSql():
    platforms = root.findall('.//cw_platform_type/platform')
    wtpcaps = root.findall('.//cw_wtp_cap/wtpcap')
    bands = root.findall('.//wl_band_type/wlband')

    f = open('wifi_radio_band.sql', 'w')

    f.write(radioBandSqlHeader)

    for p, platform in enumerate(platforms):
        for wtpcap in wtpcaps:
            if isCapTypeEqual(platform, wtpcap):
                radios = list(wtpcap.iter('radio'))
                for r, radio in enumerate(radios):
                    for b, band in enumerate(bands):
                        if isBandEqual(radio, band):
                            last = (p == len(platforms) - 1) and (r ==
                                                                  len(radios) - 1) and (b == len(bands) - 1)
                            buildRadioBandRowSql(
                                f, platform.attrib["captype"], radio.attrib["id"], b + 1, last)

    f.write(sqlFooter)


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
  `channel` int(8) NOT NULL COMMENT 'channel value'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `wifi_channel_map` WRITE;

INSERT INTO `wifi_channel_map` VALUES
"""


def buildWifiChannelRow(f, fm, oid, country, channel, last):
    if "bonding" in channel.attrib:
        channelLine = Template(
            "$band, '$bn', '$bonding', $outdoor").substitute(channel.attrib)
    else:
        channelLine = Template(
            "$band, '$bn', 'none', $outdoor").substitute(channel.attrib)

    if channel.text != None:
        channels = channel.text
    else:
        channels = ''

    f.write("(%d, '%s', %s, %s)%s\n" %
            (oid, fosVersion, country.attrib["code"], channelLine, ',' if not last else ';'))

    clist = channels.split(',')
    for ci, cv in enumerate(clist):
        clast = last and ci == len(clist) - 1
        cv = cv.replace('+', '').replace('-', '').replace('*', '')
        if cv:
            fm.write("(%d, %s)%s\n" %
                     (oid, cv, ',' if not clast else ';'))
        # else:
        #     print(clist)


def buildWifiChannelsSql():
    countries = root.findall('.//file[@name="wlchanlist.txt"]')
    country = countries[0]

    f = open('wifi_channel_key.sql', 'w')
    fm = open('wifi_channel_map.sql', 'w')

    cf = open('chanlist.xml', 'w')
    cf.write(country.text.strip())

    ctree = ET.parse('chanlist.xml')
    croot = ctree.getroot()

    countries = croot.findall('.//country')

    f.write(channelKeySqlHeader)
    fm.write(channelMapSqlHeader)

    oid = 0

    for cn, country in enumerate(countries):
        if isCountryForAp(country.attrib['code']):
            cond = './/country[@code="{0}"]/channel'.format(
                country.attrib['code'])
            channels = croot.findall(cond)
            for ch, channel in enumerate(channels):
                oid += 1
                buildWifiChannelRow(f, fm, oid, country, channel,
                                    (cn == len(countries) - 1 and ch == len(channels) - 1))

    f.write(sqlFooter)
    fm.write(sqlFooter)


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
            if isSameDictionary(c, country):
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


def buildWifiCountrySql(croot, version, countries, fosCountries):
    cs = croot.findall('.//country')

    if 0 == countries['oid']:
        f = open('wifi_countries.sql', 'w')
        f.write(countrySqlHeader)
        fo = open('wifi_fos_countries.sql', 'w')
        fo.write(fosCountrySqlHeader)
    else:
        f = open('wifi_countries.sql', 'a')
        fo = open('wifi_fos_countries.sql', 'a')

    for country in cs:
        if isCountryForAp(country.attrib['code']):
            oid = getCountryOid(country, countries)
            if 0 == oid:
                countries['oid'] += 1
                countries['rows'].append(country)
                oid = countries['oid']
                buildWifiCountryRow(f, oid, country)
            buildWifiFosCountryRow(
                fo, formatVersion(version), oid, fosCountries)


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


def run():
    path = "D:\\Workspaces\\svn\\fos_mgmt_data"
    bands = None
    countries = {'oid': 0, 'rows': []}
    fosCountries = {'oid': 0}

    platforms = {'oid': 0, 'rows': []}
    fosPlatforms = {'oid': 0}

    radios = {'oid': 0, 'rows': []}
    radioKey = {'oid': 0}
    radioMap = {'oid': 0}

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
            buildWifiCountrySql(croot, version, countries, fosCountries)
            buildWifiPlatformSql(root, version, platforms, fosPlatforms)
            buildWifiRadioSql(root, version, radios, radioKey, radioMap)

    for folder, dirs, files in os.walk("."):
        if "." == folder:
            for f in files:
                if ".sql" in f:
                    fs = open(f, 'a')
                    fs.write(sqlFooter)


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

    # buildWifiChannelsSql()
    # buildWifiRadioBandSql()

    cleanup()

    runSql(host, username, password, database)


if __name__ == "__main__":
    main()
