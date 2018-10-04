"use strict";

const Telnet = require("telnet-client");
const _ = require("lodash");

const params = {
  host: "172.16.95.49",
  port: 23,
  timeout: 5000,
  execTimeout: 5000,
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

async function telnet(conn, cmd) {
  let res = await conn.exec(cmd);
  if (params.debug) {
    let lines = _.split(res, "\n");
    lines = _.remove(lines, function(line) {
      return line.length !== 0;
    });
    if (lines.length) {
      console.log(cmd, lines);
    }
  }
  return res;
}

function getPlatforms() {
  return [
    "AP-11N",
    "220B",
    "210B",
    "222B",
    "112B",
    "320B",
    "11C",
    "14C",
    "223B",
    "28C",
    "320C",
    "221C",
    "25D",
    "222C",
    "224D",
    "214B",
    "21D",
    "24D",
    "112D",
    "223C",
    "321C",
    "S321C",
    "S322C",
    "S323C",
    "S311C",
    "S313C",
    "S321CR",
    "S322CR",
    "S323CR",
    "S421E",
    "S422E",
    "S423E",
    "421E",
    "423E",
    "221E",
    "222E",
    "223E",
    "224E",
    "S221E",
    "S223E",
    "U421E",
    "U422EV",
    "U423E",
    "U221EV",
    "U223EV",
    "U24JEV",
    "U321EV",
    "U323EV"
  ];
}

function getCountries() {
  return [
    "AL",
    "DZ",
    "AO",
    "AR",
    "AM",
    "AU",
    "AT",
    "AZ",
    "BH",
    "BD",
    "BB",
    "BY",
    "BE",
    "BZ",
    "BO",
    "BA",
    "BR",
    "BN",
    "BG",
    "KH",
    "CL",
    "CN",
    "CO",
    "CR",
    "HR",
    "CY",
    "CZ",
    "DK",
    "DO",
    "EC",
    "EG",
    "SV",
    "EE",
    "FI",
    "FR",
    "GE",
    "DE",
    "GR",
    "GL",
    "GD",
    "GU",
    "GT",
    "HT",
    "HN",
    "HK",
    "HU",
    "IS",
    "IN",
    "ID",
    "IR",
    "IE",
    "IL",
    "IT",
    "JM",
    "JO",
    "KZ",
    "KE",
    "KP",
    "KR",
    "KW",
    "LV",
    "LB",
    "LI",
    "LT",
    "LU",
    "MO",
    "MK",
    "MY",
    "MT",
    "MX",
    "MC",
    "MA",
    "MZ",
    "MM",
    "NP",
    "NL",
    "AN",
    "AW",
    "NZ",
    "NO",
    "OM",
    "PK",
    "PA",
    "PG",
    "PY",
    "PE",
    "PH",
    "PL",
    "PT",
    "PR",
    "QA",
    "RO",
    "RU",
    "RW",
    "SA",
    "RS",
    "ME",
    "SG",
    "SK",
    "SI",
    "ZA",
    "ES",
    "LK",
    "SE",
    "SD",
    "CH",
    "SY",
    "TW",
    "TZ",
    "TH",
    "TT",
    "TN",
    "TR",
    "AE",
    "UA",
    "GB",
    "US",
    "PS",
    "UY",
    "UZ",
    "VE",
    "VN",
    "YE",
    "ZB",
    "ZW",
    "JP",
    "CA"
  ];
}

function getDarrps() {
  return ["enable", "disable"];
}

async function getBands(conn, platform, radio) {
  await telnet(conn, "config wireless-controller wtp-profile");
  await telnet(conn, `edit TempProfile`);
  await telnet(conn, `config platform`);
  await telnet(conn, `set type ${platform}`);
  await telnet(conn, `end`);
  await telnet(conn, `config ${radio}`);
  let res = await telnet(conn, `set band ?`);
  await telnet(conn, "end");
  await telnet(conn, "abort");

  let lines = _.split(res, "\n");
  let bands = _.remove(lines, function(line) {
    return _.startsWith(line, "802.11");
  });
  bands = _.map(bands, function(band) {
    let o = _.split(band, " ");
    return o[0];
  });
  // console.log(bands);
  return bands;
}

async function getRadios(conn, platform) {
  await telnet(conn, "config wireless-controller wtp-profile");
  await telnet(conn, `edit TempProfile`);
  await telnet(conn, `config platform`);
  await telnet(conn, `set type ${platform}`);
  await telnet(conn, `end`);
  let res = await telnet(conn, `config ?`);
  await telnet(conn, "end");

  let lines = _.split(res, "\n");
  let radios = _.remove(lines, function(line) {
    return _.startsWith(line, "radio-");
  });
  radios = _.map(radios, function(radio) {
    let o = _.split(radio, " ");
    return o[0];
  });
  // console.log(radios);
  return radios;
}

async function getBondings(conn, platform, radio, band) {
  await telnet(conn, "config wireless-controller wtp-profile");
  await telnet(conn, `edit TempProfile`);
  await telnet(conn, `config platform`);
  await telnet(conn, `set type ${platform}`);
  await telnet(conn, `end`);
  await telnet(conn, `config ${radio}`);
  await telnet(conn, `set band ${band}`);
  let res = await telnet(conn, `set channel-bonding ?`);
  await telnet(conn, "end");
  await telnet(conn, "abort");

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
    // console.log(bondings);
    return bondings;
  }
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
  await telnet(conn, "config wireless-controller wtp-profile");
  await telnet(conn, `edit TempProfile`);
  await telnet(conn, `config platform`);
  await telnet(conn, `set type ${platform}`);
  await telnet(conn, `end`);
  await telnet(conn, `set ap-country ${country}\r\ny`);
  await telnet(conn, `config ${radio}`);
  await telnet(conn, `set band ${band}`);
  await telnet(conn, `set channel-bonding ${bonding}`);
  await telnet(conn, `set darrp ${darrp}`);

  let res = await telnet(conn, "set channel ?");
  let channels = await getChannels(res);
  await telnet(conn, "\n");
  await telnet(conn, "end");
  await telnet(conn, "abort");

  console.log(
    `'${platform}', '${country}', '${radio}', '${band}', '${bonding}', '${darrp}', ${channels}`
  );
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

async function main() {
  let start = new Date();

  const platforms = getPlatforms();
  const countries = getCountries();
  const darrps = getDarrps();

  let conn = telnetFactory(start);
  await conn.connect(params);

  for (let p = 0; p < platforms.length; ++p) {
    let platform = platforms[p];
    let radios = await getRadios(conn, platform);
    for (let r = 0; r < radios.length; ++r) {
      let radio = radios[r];
      let bands = await getBands(conn, platform, radio);
      for (let b = 0; b < bands.length; ++b) {
        let band = bands[b];
        let bondings = await getBondings(conn, platform, radio, band);
        for (let bo = 0; bo < bondings.length; ++bo) {
          let bonding = bondings[bo];
          for (let d = 0; d < darrps.length; ++d) {
            let darrp = darrps[d];
            for (let c = 0; c < countries.length; ++c) {
              let country = countries[c];
              await queryChannels(
                conn,
                platform,
                country,
                radio,
                band,
                bonding,
                darrp
              );
            }
          }
        }
      }
    }
  }

  await conn.destroy();

  let end = new Date() - start;
  console.log("Execution time: %dms", end);
}

main();

async function debug() {
  let conn = telnetFactory();
  await conn.connect(params);

  await queryChannels(
    conn,
    "AP-11N",
    "GE",
    "radio-1",
    "802.11n",
    "40MHz",
    "enable"
  );

  await conn.destroy();
}

// debug();

// 'AP-11N', 'GL', 'radio-1', '802.11n', '40MHz', 'enable', t channel
