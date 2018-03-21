package main

import (
	"bufio"
	"bytes"
	"encoding/binary"
	"fmt"
	"net"
)

type (
	// Preamble Preamble
	Preamble struct {
		preamble uint8
	}

	// DiscoveryRequest Discovery Request
	DiscoveryRequest struct {
		preamble      Preamble
		discoveryType uint8
	}
)

// SetVersion Set Preamble Version
func (p *Preamble) SetVersion(version uint8) {
	p.preamble |= version << 4
}

// GetVersion Get Preamble Version
func (p *Preamble) GetVersion() uint8 {
	return p.preamble >> 4
}

const (
	version      = 0
	capwapHeader = 0
)

const (
	cwMsgElementDiscoveryTypeBroadcast  = 0
	cwMsgElementDiscoveryTypeConfigured = 1
)

func cwWtpEnterDiscovery() {
	p := Preamble{}
	p.SetVersion(version)

	r := DiscoveryRequest{
		preamble:      p,
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
