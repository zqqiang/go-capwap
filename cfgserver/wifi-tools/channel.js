"use strict";

const fs = require("fs");
const Telnet = require("telnet-client");
const _ = require("lodash");

const params = {
  host: "172.16.95.49",
  port: 23,
  timeout: 15000,
  execTimeout: 15000,
  username: "admin",
  password: "admin",
  pageSeparator: "--More--",
  // debug: true
  debug: false
};

async function getChannels(out) {
  let lines = _.split(out, "\n");
  let channels = _.trimStart(lines[0], "*wireless_channel    <");
  channels = _.trimEnd(channels, ">");
  return channels;
}

let count = 0;

async function telnet(conn, cmd) {
  let res = await conn.exec(cmd);
  if (params.debug) {
    let lines = _.split(res, "\n");
    lines = _.remove(lines, function(line) {
      return line.length !== 0;
    });
    if (lines.length) {
      console.log(count++, cmd, lines);
    }
  }
  return res;
}

function getPlatforms() {
  return [
    { key: "AP-11N", name: "Default 11n AP" },
    { key: "220B", name: "FAP220B" },
    { key: "210B", name: "FAP210B" },
    { key: "222B", name: "FAP222B" },
    { key: "112B", name: "FAP112B" },
    { key: "320B", name: "FAP320B" },
    { key: "11C", name: "FAP11C" },
    { key: "14C", name: "FAP14C" },
    { key: "223B", name: "FAP223B" },
    { key: "28C", name: "FAP28C" },
    { key: "320C", name: "FAP320C" },
    { key: "221C", name: "FAP221C" },
    { key: "25D", name: "FAP25D" },
    { key: "222C", name: "FAP222C" },
    { key: "224D", name: "FAP224D" },
    { key: "214B", name: "FK214B" },
    { key: "21D", name: "FAP21D" },
    { key: "24D", name: "FAP24D" },
    { key: "112D", name: "FAP112D" },
    { key: "223C", name: "FAP223C" },
    { key: "321C", name: "FAP321C" },
    { key: "S321C", name: "FAPS321C" },
    { key: "S322C", name: "FAPS322C" },
    { key: "S323C", name: "FAPS323C" },
    { key: "S311C", name: "FAPS311C" },
    { key: "S313C", name: "FAPS313C" },
    { key: "S321CR", name: "FAPS321CR" },
    { key: "S322CR", name: "FAPS322CR" },
    { key: "S323CR", name: "FAPS323CR" },
    { key: "S421E", name: "FAPS421E" },
    { key: "S422E", name: "FAPS422E" },
    { key: "S423E", name: "FAPS423E" },
    { key: "421E", name: "FAP421E" },
    { key: "423E", name: "FAP423E" },
    { key: "221E", name: "FAP221E" },
    { key: "222E", name: "FAP222E" },
    { key: "223E", name: "FAP223E" },
    { key: "224E", name: "FAP224E" },
    { key: "S221E", name: "FAPS221E" },
    { key: "S223E", name: "FAPS223E" },
    { key: "U421E", name: "FAPU421EV" },
    { key: "U422EV", name: "FAPU422EV" },
    { key: "U423E", name: "FAPU423EV" },
    { key: "U221EV", name: "FAPU221EV" },
    { key: "U223EV", name: "FAPU223EV" },
    { key: "U24JEV", name: "FAPU24JEV" },
    { key: "U321EV", name: "FAPU321EV" },
    { key: "U323EV", name: "FAPU323EV" }
  ];
}

async function buildWifiPlatformsSql() {
  const sql = `
DROP TABLE IF EXISTS 'wifi_platforms';

CREATE TABLE 'wifi_platforms' (
  'oid' int(11) NOT NULL COMMENT 'platform oid',
  'name' char(6) DEFAULT NULL COMMENT 'platform name',
  'display' char(16) DEFAULT NULL COMMENT 'platform gui display',
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES 'wifi_platforms' WRITE;

INSERT INTO 'wifi_platforms' VALUES `;

  try {
    await fs.writeFileSync("wifi_platforms.sql", sql, "utf8");
  } catch (err) {
    console.log(err);
  }
  let platforms = getPlatforms();
  for(let p = 0; p < platforms.length; ++p){
    try {
      let sep = p !== platforms.length - 1 ? ',': ';';
      let platform = platforms[p];
      await fs.appendFileSync("wifi_platforms.sql", `\r\n    (${p}, '${platform.key}', '${platform.name}')${sep}`, "utf8");
    } catch (err) {
      console.log(err);
    }
  }

  try {
    await fs.appendFileSync("wifi_platforms.sql", `\r\n\r\nUNLOCK TABLES;`, "utf8");
  } catch (err) {
    console.log(err);
  }
}

function getCountries() {
  return [
    { key: "AA", code: 1 },
    { key: "AF", code: 4 },
    { key: "AL", code: 8 },
    { key: "AQ", code: 10 },
    { key: "DZ", code: 12 },
    { key: "AS", code: 16 },
    { key: "AD", code: 20 },
    { key: "AO", code: 24 },
    { key: "AG", code: 28 },
    { key: "AZ", code: 31 },
    { key: "AR", code: 32 },
    { key: "AU", code: 36 },
    { key: "AT", code: 40 },
    { key: "BS", code: 44 },
    { key: "BH", code: 48 },
    { key: "BD", code: 50 },
    { key: "AM", code: 51 },
    { key: "BB", code: 52 },
    { key: "BE", code: 56 },
    { key: "BM", code: 60 },
    { key: "BT", code: 64 },
    { key: "BO", code: 68 },
    { key: "BA", code: 70 },
    { key: "BW", code: 72 },
    { key: "BV", code: 74 },
    { key: "BR", code: 76 },
    { key: "BZ", code: 84 },
    { key: "IO", code: 86 },
    { key: "SB", code: 90 },
    { key: "VG", code: 92 },
    { key: "BN", code: 96 },
    { key: "BG", code: 100 },
    { key: "MM", code: 104 },
    { key: "BI", code: 108 },
    { key: "BY", code: 112 },
    { key: "KH", code: 116 },
    { key: "CM", code: 120 },
    { key: "CA", code: 124 },
    { key: "CV", code: 132 },
    { key: "KY", code: 136 },
    { key: "CF", code: 140 },
    { key: "LK", code: 144 },
    { key: "TD", code: 148 },
    { key: "CL", code: 152 },
    { key: "CN", code: 156 },
    { key: "TW", code: 158 },
    { key: "CX", code: 162 },
    { key: "CC", code: 166 },
    { key: "CO", code: 170 },
    { key: "KM", code: 174 },
    { key: "YT", code: 175 },
    { key: "CG", code: 178 },
    { key: "CD", code: 180 },
    { key: "CK", code: 184 },
    { key: "CR", code: 188 },
    { key: "HR", code: 191 },
    { key: "CU", code: 192 },
    { key: "CY", code: 196 },
    { key: "CZ", code: 203 },
    { key: "BJ", code: 204 },
    { key: "DK", code: 208 },
    { key: "DM", code: 212 },
    { key: "DO", code: 214 },
    { key: "EC", code: 218 },
    { key: "SV", code: 222 },
    { key: "GQ", code: 226 },
    { key: "ET", code: 231 },
    { key: "ER", code: 232 },
    { key: "EE", code: 233 },
    { key: "FO", code: 234 },
    { key: "FK", code: 238 },
    { key: "GS", code: 239 },
    { key: "FJ", code: 242 },
    { key: "FI", code: 246 },
    { key: "FX", code: 249 },
    { key: "FR", code: 250 },
    { key: "GF", code: 254 },
    { key: "PF", code: 258 },
    { key: "TF", code: 260 },
    { key: "DJ", code: 262 },
    { key: "GA", code: 266 },
    { key: "GE", code: 268 },
    { key: "GM", code: 270 },
    { key: "DE", code: 276 },
    { key: "GH", code: 288 },
    { key: "GI", code: 292 },
    { key: "KI", code: 296 },
    { key: "GR", code: 300 },
    { key: "GL", code: 304 },
    { key: "GD", code: 308 },
    { key: "GP", code: 312 },
    { key: "GU", code: 316 },
    { key: "GT", code: 320 },
    { key: "GN", code: 324 },
    { key: "GY", code: 328 },
    { key: "HT", code: 332 },
    { key: "HM", code: 334 },
    { key: "VA", code: 336 },
    { key: "HN", code: 340 },
    { key: "HK", code: 344 },
    { key: "HU", code: 348 },
    { key: "IS", code: 352 },
    { key: "IN", code: 356 },
    { key: "ID", code: 360 },
    { key: "IR", code: 364 },
    { key: "IQ", code: 368 },
    { key: "IE", code: 372 },
    { key: "IL", code: 376 },
    { key: "IT", code: 380 },
    { key: "CI", code: 384 },
    { key: "JM", code: 388 },
    { key: "JP", code: 392 },
    { key: "KZ", code: 398 },
    { key: "JO", code: 400 },
    { key: "KE", code: 404 },
    { key: "KP", code: 408 },
    { key: "KR", code: 410 },
    { key: "KW", code: 414 },
    { key: "KG", code: 417 },
    { key: "LA", code: 418 },
    { key: "LB", code: 422 },
    { key: "LS", code: 426 },
    { key: "LV", code: 428 },
    { key: "LR", code: 430 },
    { key: "LY", code: 434 },
    { key: "LI", code: 438 },
    { key: "LT", code: 440 },
    { key: "LU", code: 442 },
    { key: "MO", code: 446 },
    { key: "MG", code: 450 },
    { key: "MW", code: 454 },
    { key: "MY", code: 458 },
    { key: "MV", code: 462 },
    { key: "ML", code: 466 },
    { key: "MT", code: 470 },
    { key: "MQ", code: 474 },
    { key: "MR", code: 478 },
    { key: "MU", code: 480 },
    { key: "MX", code: 484 },
    { key: "MC", code: 492 },
    { key: "MN", code: 496 },
    { key: "MD", code: 498 },
    { key: "MS", code: 500 },
    { key: "MA", code: 504 },
    { key: "MZ", code: 508 },
    { key: "OM", code: 512 },
    { key: "NA", code: 516 },
    { key: "NR", code: 520 },
    { key: "NP", code: 524 },
    { key: "NL", code: 528 },
    { key: "AN", code: 530 },
    { key: "AW", code: 533 },
    { key: "NC", code: 540 },
    { key: "VU", code: 548 },
    { key: "NZ", code: 554 },
    { key: "NI", code: 558 },
    { key: "NE", code: 562 },
    { key: "NG", code: 566 },
    { key: "NU", code: 570 },
    { key: "NF", code: 574 },
    { key: "NO", code: 578 },
    { key: "MP", code: 580 },
    { key: "UM", code: 581 },
    { key: "FM", code: 583 },
    { key: "MH", code: 584 },
    { key: "PW", code: 585 },
    { key: "PK", code: 586 },
    { key: "PA", code: 591 },
    { key: "PG", code: 598 },
    { key: "PY", code: 600 },
    { key: "PE", code: 604 },
    { key: "PH", code: 608 },
    { key: "PN", code: 612 },
    { key: "PL", code: 616 },
    { key: "PT", code: 620 },
    { key: "GW", code: 624 },
    { key: "PR", code: 630 },
    { key: "QA", code: 634 },
    { key: "RE", code: 638 },
    { key: "RO", code: 642 },
    { key: "RU", code: 643 },
    { key: "RW", code: 646 },
    { key: "SH", code: 654 },
    { key: "KN", code: 659 },
    { key: "AI", code: 660 },
    { key: "LC", code: 662 },
    { key: "PM", code: 666 },
    { key: "VC", code: 670 },
    { key: "SM", code: 674 },
    { key: "ST", code: 678 },
    { key: "SA", code: 682 },
    { key: "SN", code: 686 },
    { key: "SC", code: 690 },
    { key: "SL", code: 694 },
    { key: "SG", code: 702 },
    { key: "SK", code: 703 },
    { key: "VN", code: 704 },
    { key: "SI", code: 705 },
    { key: "SO", code: 706 },
    { key: "ZA", code: 710 },
    { key: "ZW", code: 716 },
    { key: "ES", code: 724 },
    { key: "SS", code: 728 },
    { key: "SD", code: 729 },
    { key: "EH", code: 732 },
    { key: "SR", code: 740 },
    { key: "SJ", code: 744 },
    { key: "SZ", code: 748 },
    { key: "SE", code: 752 },
    { key: "CH", code: 756 },
    { key: "SY", code: 760 },
    { key: "TJ", code: 762 },
    { key: "TH", code: 764 },
    { key: "TG", code: 768 },
    { key: "TK", code: 772 },
    { key: "TO", code: 776 },
    { key: "TT", code: 780 },
    { key: "AE", code: 784 },
    { key: "TN", code: 788 },
    { key: "TR", code: 792 },
    { key: "TM", code: 795 },
    { key: "TC", code: 796 },
    { key: "TV", code: 798 },
    { key: "UG", code: 800 },
    { key: "UA", code: 804 },
    { key: "EG", code: 818 },
    { key: "GB", code: 826 },
    { key: "TZ", code: 834 },
    { key: "US", code: 840 },
    { key: "VI", code: 850 },
    { key: "BF", code: 854 },
    { key: "UY", code: 858 },
    { key: "UZ", code: 860 },
    { key: "VE", code: 862 },
    { key: "WF", code: 876 },
    { key: "WS", code: 882 },
    { key: "YE", code: 887 },
    { key: "YU", code: 891 },
    { key: "ZM", code: 894 }
  ];
}

function getDarrps() {
  return ["enable", "disable"];
}

function getDarrpCode(darrp) {
  const darrpMap = ["enable", "disable"];
  return _.indexOf(darrpMap, darrp);
}

async function getBands(conn) {
  let res = await telnet(conn, `set band ?`);

  let lines = _.split(res, "\n");
  let bands = _.remove(lines, function(line) {
    return _.startsWith(line, "802.11");
  });
  bands = _.map(bands, function(band) {
    let o = _.split(band, " ");
    return o[0];
  });
  return bands;
}

function getBandCode(band) {
  const bandMap = [
    "802.11a",
    "802.11b",
    "802.11g",
    "802.11n",
    "802.11n-5G",
    "802.11n,g-only",
    "802.11g-only",
    "802.11n-only",
    "802.11n-5G-only",
    "802.11ac",
    "802.11ac,n-only",
    "802.11ac-only"
  ];

  return _.indexOf(bandMap, band);
}

async function getRadios(conn) {
  let res = await telnet(conn, `config ?`);

  let lines = _.split(res, "\n");
  let radios = _.remove(lines, function(line) {
    return _.startsWith(line, "radio-");
  });
  radios = _.map(radios, function(radio) {
    let o = _.split(radio, " ");
    return o[0];
  });
  return radios;
}

function getRadioCode(radio) {
  const radioMap = ["radio-1", "radio-2"];
  return _.indexOf(radioMap, radio);
}

async function getBondings(conn) {
  let res = await telnet(conn, `set channel-bonding ?`);

  let lines = _.split(res, "\n");
  if (lines[0].includes(`command parse error`)) {
    return [];
  } else {
    let bondings = _.remove(lines, function(line) {
      return line.includes("MHz");
    });
    bondings = _.map(bondings, function(bonding) {
      let o = _.split(bonding, " ");
      return o[0];
    });
    return bondings;
  }
}

function getBondingCode(bonding) {
  const bondingMap = ["20MHz", "40MHz", "80MHz"];
  return _.indexOf(bondingMap, bonding);
}

async function queryChannels(conn) {
  let res = await telnet(conn, "set channel ?");
  let channels = await getChannels(res);
  return channels;
}

function telnetFactory(start) {
  let conn = new Telnet();

  conn.on("timeout", function() {
    console.log("connection timeout!");
    conn.end();
  });

  conn.on("end", function() {
    console.log("connection end!");
    let end = new Date() - start;
    console.log("Execution time: %dms", end);
  });

  conn.on("close", function() {
    if (params.debug) {
      console.log("connection closed!");
    }
  });

  conn.on("error", function() {
    console.log("connection error!");
  });

  return conn;
}

async function buildWifiChannelsSql() {
  const sql = `
DROP TABLE IF EXISTS 'wifi_channels';

CREATE TABLE 'wifi_channels' (
  'country' int(11) NOT NULL COMMENT 'country numeric code',
  'platform' int(11) NOT NULL COMMENT 'platform oid',
  'radio' smallint(5) DEFAULT NULL COMMENT 'radio-1: 1, radio-2: 2',
  'band' int(11) NOT NULL COMMENT 'band oid',
  'bonding' smallint(5) DEFAULT NULL COMMENT 'high-throughput band-wide mode(0:20MHz,1:40MHz,2:80MHz)',
  'darrp' tinyint(1) DEFAULT NULL COMMENT 'if darrp has been choose.',
  'channels' varchar(128) NOT NULL COMMENT 'channel list, eg. 1,2,3,4,...'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES 'wifi_channels' WRITE;

INSERT INTO 'wifi_channels' VALUES `;

  try {
    fs.writeFileSync("wifi_channels.sql", sql, "utf8");
  } catch (err) {
    console.log(err);
  }
}

async function buildWifiChannelsSqlEnd() {
  const end = `
(0, 0, 0, 0, 0, 0, '');

UNLOCK TABLES;`;

  try {
    fs.appendFileSync("wifi_channels.sql", end, "utf8");
  } catch (err) {
    console.log(err);
  }
}

async function sqlAppend(
  country,
  platform,
  radio,
  band,
  bonding,
  darrp,
  channels
) {
  let sql = `\r\n(${country}, ${platform}, ${radio}, ${band}, ${bonding}, ${darrp}, '${channels}'),`;

  try {
    fs.appendFileSync("wifi_channels.sql", sql, "utf8");
  } catch (err) {
    console.log(err);
  }
}

async function main() {
  let start = new Date();

  process.on("SIGINT", code => {
    buildWifiChannelsSqlEnd();
    let end = new Date() - start;
    console.log("Execution time: %dms", end);
    process.exit(0);
  });

  const platforms = getPlatforms();
  const countries = getCountries();
  const darrps = getDarrps();

  await buildWifiChannelsSql();

  let conn = telnetFactory(start);
  await conn.connect(params);

  await telnet(
    conn,
    "config wireless-controller wtp-profile\r\nedit temp-profile"
  );

  for (let c = 0; c < countries.length; ++c) {
    let country = countries[c];
    await telnet(conn, `set ap-country ${country.key}\r\ny`);

    for (let p = 0; p < platforms.length; ++p) {
      let platform = platforms[p];

      await telnet(conn, `config platform`);
      await telnet(conn, `set type ${platform.key}`);
      await telnet(conn, `end`);
      let radios = await getRadios(conn);

      for (let r = 0; r < radios.length; ++r) {
        let radio = radios[r];

        await telnet(conn, `config ${radio}`);

        let bands = await getBands(conn);
        for (let b = 0; b < bands.length; ++b) {
          let band = bands[b];

          await telnet(conn, `set band ${band}`);

          let bondings = await getBondings(conn);
          for (let bo = 0; bo < bondings.length; ++bo) {
            let bonding = bondings[bo];

            await telnet(conn, `set channel-bonding ${bonding}`);

            for (let d = 0; d < darrps.length; ++d) {
              let darrp = darrps[d];

              await telnet(conn, `set darrp ${darrp}`);

              let channels = await queryChannels(conn);

              console.log(
                `'${++count}'. ${country.key}', '${
                  platform.key
                }', '${radio}', '${band}', '${bonding}', '${darrp}', '${channels}'`
              );

              await sqlAppend(
                country.code,
                p,
                getRadioCode(radio),
                getBandCode(band),
                getBondingCode(bonding),
                getDarrpCode(darrp),
                channels
              );
            }
          }
        }

        await telnet(conn, `abort`);
      }
    }
  }

  await telnet(conn, `abort`);

  await conn.destroy();

  buildWifiChannelsSqlEnd();
  let end = new Date() - start;
  console.log("Execution time: %dms", end);
}

// main();

buildWifiPlatformsSql();
