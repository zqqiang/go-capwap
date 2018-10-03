"use strict";

const Telnet = require("telnet-client");
const _ = require("lodash");

const params = {
  host: "172.16.95.49",
  port: 23,
  timeout: 1500,
  username: "admin",
  password: "admin",
  pageSeparator: "--More--",
  debug: true
};

async function getChannels(out) {
  let lines = _.split(out, "\n");
  let channels = _.trimStart(lines[0], "*wireless_channel    <");
  channels = _.trimEnd(channels, ">");
  return channels;
}

function getPlatforms() {
  return [
    // "AP-11N",
    // "220B",
    // "210B",
    // "222B",
    // "112B",
    // "320B",
    // "11C",
    // "14C",
    // "223B",
    // "28C",
    "320C"
    // "221C",
    // "25D",
    // "222C",
    // "224D",
    // "214B",
    // "21D",
    // "24D",
    // "112D",
    // "223C",
    // "321C",
    // "S321C",
    // "S322C",
    // "S323C",
    // "S311C",
    // "S313C",
    // "S321CR",
    // "S322CR",
    // "S323CR",
    // "S421E",
    // "S422E",
    // "S423E",
    // "421E",
    // "423E",
    // "221E",
    // "222E",
    // "223E",
    // "224E",
    // "S221E",
    // "S223E",
    // "U421E",
    // "U422EV",
    // "U423E",
    // "U221EV",
    // "U223EV",
    // "U24JEV",
    // "U321EV",
    // "U323EV"
  ];
}

function getCountries() {
  return [
    // "AL",
    // "DZ",
    // "AO",
    // "AR",
    // "AM",
    // "AU",
    // "AT",
    // "AZ",
    // "BH",
    // "BD",
    // "BB",
    // "BY",
    // "BE",
    // "BZ",
    // "BO",
    // "BA",
    // "BR",
    // "BN",
    // "BG",
    // "KH",
    // "CL",
    // "CN",
    // "CO",
    // "CR",
    // "HR",
    // "CY",
    // "CZ",
    // "DK",
    // "DO",
    // "EC",
    // "EG",
    // "SV",
    // "EE",
    // "FI",
    // "FR",
    // "GE",
    // "DE",
    // "GR",
    // "GL",
    // "GD",
    // "GU",
    // "GT",
    // "HT",
    // "HN",
    // "HK",
    // "HU",
    // "IS",
    // "IN",
    // "ID",
    // "IR",
    // "IE",
    // "IL",
    // "IT",
    // "JM",
    // "JO",
    // "KZ",
    // "KE",
    // "KP",
    // "KR",
    // "KW",
    // "LV",
    // "LB",
    // "LI",
    // "LT",
    // "LU",
    // "MO",
    // "MK",
    // "MY",
    // "MT",
    // "MX",
    // "MC",
    // "MA",
    // "MZ",
    // "MM",
    // "NP",
    // "NL",
    // "AN",
    // "AW",
    // "NZ",
    // "NO",
    // "OM",
    // "PK",
    // "PA",
    // "PG",
    // "PY",
    // "PE",
    // "PH",
    // "PL",
    // "PT",
    // "PR",
    // "QA",
    // "RO",
    // "RU",
    // "RW",
    // "SA",
    // "RS",
    // "ME",
    // "SG",
    // "SK",
    // "SI",
    // "ZA",
    // "ES",
    // "LK",
    // "SE",
    // "SD",
    // "CH",
    // "SY",
    // "TW",
    // "TZ",
    // "TH",
    // "TT",
    // "TN",
    // "TR",
    // "AE",
    // "UA",
    // "GB",
    // "US",
    // "PS",
    // "UY",
    // "UZ",
    // "VE",
    // "VN",
    // "YE",
    // "ZB",
    // "ZW",
    // "JP",
    "CA"
  ];
}

function getRadio1Bands() {
  return [
    "802.11b",
    "802.11g",
    "802.11n",
    "802.11n, g - only",
    "802.11g - only",
    "802.11n - only"
  ];
}

function getRadio2Bands() {
  return [
    "802.11a",
    "802.11n - 5G",
    "802.11ac",
    "802.11n - 5G - only",
    "802.11ac, n - only",
    "802.11ac - only"
  ];
}

function getRadio1Bonding() {
  return ["40MHz", "20MHz"];
}

function getRadio2Bonding() {
  return ["80MHz", "40MHz", "20MHz"];
}

function getDarrps() {
  return ["enable", "disable"];
}

async function queryChannels(
  conn,
  platform,
  country,
  radio,
  band,
  bonding,
  darrp
) {
  await conn.exec("config wireless-controller wtp-profile");
  await conn.exec(`edit TempProfile`);
  await conn.exec(`config platform`);
  await conn.exec(`set type ${platform}`);
  await conn.exec(`end`);
  await conn.exec(`set ap-country ${country}\r\ny`);
  await conn.exec(`config ${radio}`);
  await conn.exec(`set band ${band}`);
  await conn.exec(`set channel-bonding ${bonding}`);
  await conn.exec(`set darrp ${darrp}`);

  let res = await conn.exec("set channel ?");
  let channels = await getChannels(res);
  await conn.exec("\n");
  await conn.exec("end");
  await conn.exec("abort");

  console.log(
    `${platform}, ${country}, ${radio}, '${band}', ${bonding}, ${darrp}, ${channels}`
  );
}

async function main() {
  const platforms = getPlatforms();
  const countries = getCountries();
  const radio1Bands = getRadio1Bands();
  const radio2Bands = getRadio2Bands();
  const radio1Bonding = getRadio1Bonding();
  const radio2Bonding = getRadio2Bonding();
  const darrps = getDarrps();

  let conn = new Telnet();
  await conn.connect(params);

  for (let p = 0; p < platforms.length; ++p) {
    let platform = platforms[p];
    for (let c = 0; c < countries.length; ++c) {
      let country = countries[c];
      for (let ba = 0; ba < radio1Bands.length; ++ba) {
        let band = radio1Bands[ba];
        for (let bo = 0; bo < radio1Bonding.length; ++bo) {
          let bonding = radio1Bonding[bo];
          for (let d = 0; d < darrps.length; ++d) {
            let darrp = darrps[d];
            await queryChannels(
              conn,
              platform,
              country,
              "radio-1",
              band,
              bonding,
              darrp
            );
          }
        }
      }
      for (let ba = 0; ba < radio2Bands.length; ++ba) {
        let band = radio1Bands[ba];
        for (let bo = 0; bo < radio2Bonding.length; ++bo) {
          let bonding = radio2Bonding[bo];
          for (let d = 0; d < darrps.length; ++d) {
            let darrp = darrps[d];
            await queryChannels(
              conn,
              platform,
              country,
              "radio-2",
              band,
              bonding,
              darrp
            );
          }
        }
      }
    }
  }

  await conn.end();
}

main();
