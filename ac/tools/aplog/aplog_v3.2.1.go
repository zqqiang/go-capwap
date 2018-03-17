package main

import (
	"bytes"
	"encoding/binary"
	"errors"
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
	"time"
)

type EventLog struct {
	account   uint64
	logDbHost uint32
	logtype   uint8
	reserved1 [1]uint8
	length    uint16

	reserved2 [5]uint8
	reserved3 [3]uint8

	timestamp int64
	eventType [16]uint8
	body      [48]uint8
}

type TrafficLog struct {
	account   uint64
	logDbHost uint32
	logtype   uint8
	reserved1 [1]uint8
	length    uint16

	reserved2 [5]uint8
	reserved3 [3]uint8

	timestamp int64
	win       int64
	body      [56]uint8
}

func Ip2long(ipAddr string) (uint32, error) {
	ip := net.ParseIP(ipAddr)
	if ip == nil {
		return 0, errors.New("wrong ipAddr format")
	}
	ip = ip.To4()
	return binary.LittleEndian.Uint32(ip), nil
}

func sendLog(account uint64, logType uint8, ip string) {
	c, err := net.Dial("unixgram", "/tmp/cwLoggerSocket")
	if err != nil {
		log.Fatal("Dial error: ", err)
	}
	defer c.Close()

	host, _ := Ip2long(ip)
	t := time.Now().Unix()

	eLog := EventLog{
		account:   account,
		logDbHost: host,
		logtype:   0,
		length:    72,

		timestamp: t,
		eventType: [16]uint8{'a', 'p'},
	}

	tLog := TrafficLog{
		account:   account,
		logDbHost: host,
		logtype:   1,
		length:    72,

		timestamp: t,
		win:       60,
	}

	buf := &bytes.Buffer{}
	if logType == 0 {
		err = binary.Write(buf, binary.LittleEndian, eLog)
	} else {
		err = binary.Write(buf, binary.LittleEndian, tLog)
	}
	if err != nil {
		panic(err)
	}
	fmt.Printf("% x\n", buf.Bytes())

	_, err = c.Write(buf.Bytes())
	if err != nil {
		log.Fatal("Write error: ", err)
	}
}

const (
	EVENT   = 0
	TRAFFIC = 1
	SUMMARY = 2
)

func main() {
	argsWithoutProg := os.Args[1:]
	if len(argsWithoutProg) != 2 {
		panic("usage:./aplog <ap_server> <account_oid>")
	}

	host := argsWithoutProg[0]

	account, err := strconv.ParseUint(argsWithoutProg[1], 10, 64)
	if err != nil {
		panic(err)
	}

	ticker := time.NewTicker(1000 * time.Millisecond)
	go func() {
		for t := range ticker.C {
			fmt.Println("Send log at", t)
			sendLog(account, EVENT, host)
			sendLog(account, TRAFFIC, host)
		}
	}()

	time.Sleep(2 * time.Hour)
	ticker.Stop()
	fmt.Println("Sender stopped")
}
