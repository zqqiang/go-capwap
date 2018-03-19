package main

import (
	"bufio"
	"bytes"
	"encoding/binary"
	"fmt"
	"net"
)

type (
	discoveryReq struct {
		discoveryType uint8
	}
)

const (
	cwMsgElementDiscoveryTypeBroadcast  = 0
	cwMsgElementDiscoveryTypeConfigured = 1
)

func cwWtpEnterDiscovery() {
	r := discoveryReq{
		discoveryType: cwMsgElementDiscoveryTypeConfigured,
	}
	buf := &bytes.Buffer{}
	if err := binary.Write(buf, binary.LittleEndian, r); err != nil {
		panic(err)
	}

	fmt.Printf("% x\n", buf.Bytes())
}

func startWtp() {
	cwWtpEnterDiscovery()
}

func tcp() {
	conn, err := net.Dial("tcp", "localhost:5246")
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	fmt.Fprintf(conn, "GET / HTTP/1.0\r\n\r\n")
	status, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	fmt.Printf("ap receive: %+v\n", status)
}

func main() {
	startWtp()
}
