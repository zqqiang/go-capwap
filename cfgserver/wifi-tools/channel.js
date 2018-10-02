"use strict";

const Telnet = require("telnet-client");
const _ = require("lodash");

async function getChannels(out) {
  let lines = _.split(out, '\n')
  let channels = _.trimStart(lines[0], '*wireless_channel    <')
  channels = _.trimEnd(channels, '>')
  console.log(channels)
  return channels
}

async function run() {
  let connection = new Telnet();

  let params = {
    host: "172.16.95.49",
    port: 23,
    timeout: 1500,
    username: "admin",
    password: "admin"
  };

  await connection.connect(params);

  await connection.exec("config wireless-controller wtp-profile");

  await connection.exec("edit FP320C");

  await connection.exec("config radio-1");

  let res = await connection.exec("set channel ?");

  await connection.exec("end");

  await getChannels(res)

  await connection.exec("config radio-2");

  res = await connection.exec("set channel ?");

  await getChannels(res)

  await connection.exec("end");

  await connection.end();
}

run();
