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
	"unsafe"
)

type EventLog struct {
	account   uint64
	logtype   uint8
	reserved1 [1]uint8
	length    uint16
	reserved2 [4]uint8

	reserved3 [5]uint8
	reserved4 [3]uint8

	timestamp int64
	eventType [16]uint8
	subType   [32]uint8
	ap        [16]uint8
}

type TrafficLog struct {
	account   uint64
	logtype   uint8
	reserved1 [1]uint8
	length    uint16
	reserved2 [4]uint8

	reserved3 [5]uint8
	reserved4 [3]uint8

	timestamp int64
	win       int64
	ap        [16]uint8
	ssid      [64]uint8
	rId       uint16
	wId       uint16
	clientMac [6]uint8
	user      [32]uint8
	group     [32]uint8
	auth      [32]uint8
	sent      uint64
	rcvd      uint64
}

func Ip2long(ipAddr string) (uint32, error) {
	ip := net.ParseIP(ipAddr)
	if ip == nil {
		return 0, errors.New("wrong ipAddr format")
	}
	ip = ip.To4()
	return binary.LittleEndian.Uint32(ip), nil
}

func sendLog(account uint64, logType uint8) {
	c, err := net.Dial("unixgram", "/tmp/cwLoggerSocket")
	if err != nil {
		log.Fatal("Dial error: ", err)
	}
	defer c.Close()

	t := time.Now().Unix()

	eLog := EventLog{
		account: account,
		logtype: 0,

		timestamp: t,
		eventType: [16]uint8{'a', 'p'},
		subType:   [32]uint8{'a', 'p', '-', 's', 't', 'a', 't', 'u', 's'},
		ap:        [16]uint8{'P', 'S', '3', '1', '1', 'C', '3', 'U', '1', '5', '0', '0', '0', '0', '0', '7'},
	}

	eLog.length = uint16(unsafe.Sizeof(eLog) - 24)

	tLog := TrafficLog{
		account: account,
		logtype: 1,
		length:  218,

		timestamp: t,
		win:       60,
		ap:        [16]uint8{'f', 'a', 'k', 'e', '-', 'a', 'p'},
		ssid:      [64]uint8{'f', 'a', 'k', 'e', '-', 's', 's', 'i', 'd'},
		rId:       1,
		wId:       1,
		clientMac: [6]uint8{0xff, 0x11, 0x22, 0x33, 0x44, 0x55},
		user:      [32]uint8{'f', 'a', 'k', 'e', '-', 'u', 's', 'e', 'r'},
		group:     [32]uint8{'f', 'a', 'k', 'e', '-', 'g', 'r', 'o', 'u', 'p'},
		auth:      [32]uint8{'f', 'a', 'k', 'e', '-', 'a', 'u', 't', 'h'},
		sent:      0x0100000000000000,
		rcvd:      0x0200000000000000,
	}

	// tLog.length = uint16(unsafe.Sizeof(tLog) - 24 - 8)

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
	if len(argsWithoutProg) != 1 {
		panic("usage:./aplog <account_oid>")
	}

	account, err := strconv.ParseUint(argsWithoutProg[0], 10, 64)
	if err != nil {
		panic(err)
	}

	ticker := time.NewTicker(1000 * time.Millisecond)
	go func() {
		for t := range ticker.C {
			fmt.Println("Send log at", t)
			sendLog(account, EVENT)
			sendLog(account, TRAFFIC)
		}
	}()

	time.Sleep(2 * time.Hour)
	ticker.Stop()
	fmt.Println("Sender stopped")
}
