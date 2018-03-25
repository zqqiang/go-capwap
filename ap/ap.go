package main

import (
	"fmt"
	"net"
)

func cwWtpEnterDiscovery() {
	p := Preamble{0, CapwapHeader}
	pb, err := p.Marshal()
	if err != nil {
		panic(err)
	}
	fmt.Printf("%s raw[% x]\n", p.String(), pb)

	h := Header{
		2,
		1,
		IEEE80211,
		HeaderFlags{0, 0, 0, 0, 0, 0, 0},
		0,
		0,
		0,
	}
	hb, err := h.Marshal()
	if err != nil {
		panic(err)
	}
	fmt.Printf("%s raw[% x]\n", h.String(), hb)

	tcp(append(pb, hb...))
}

func startWtp() {
	cwWtpEnterDiscovery()
}

func tcp(b []byte) {
	conn, err := net.Dial("tcp", "localhost:5246")
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	n, err := conn.Write(b)
	if err != nil {
		panic(err)
	}
	fmt.Printf("ap send: len %d raw[% x]\n", n, b)

	var reply = make([]byte, 1024)
	rn, err := conn.Read(reply)
	if err != nil {
		panic(err)
	}
	fmt.Printf("ap recv: len %d raw[% x]\n", rn, reply[:rn])
}

func main() {
	startWtp()
}
