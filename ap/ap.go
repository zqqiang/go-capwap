package main

import (
	"fmt"
	"net"
)

type State int

const (
	CWEnterDiscovery State = iota + 1
	CWEnterSulking
	CWEnterJoin
	CWEnterConfigure
	CWEnterDataCheck
	CWEnterRun
	CWEnterReset
	CWQuit
)

const (
	CWMaxDiscoveries = 10
)

type CWACDescriptor struct {
}

var CWACList []CWACDescriptor

func CWWTPEnterDiscovery() State {
	fmt.Println("######### Discovery State #########")

	CWDiscoveryCount := 0

	for {
		if CWDiscoveryCount == CWMaxDiscoveries {
			return CWEnterSulking
		}
		for i := 0; i < len(CWACList); i++ {

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

			c := ControlHeader{
				MessageType{0, 1},
				67,
				351,
				0,
			}
			cb, err := c.Marshal()
			if err != nil {
				panic(err)
			}
			fmt.Printf("%s raw[% x]\n", c.String(), cb)

			s := append(pb, hb...)
			s = append(s, cb...)

			tcp(s)

		}
		break
	}

	return CWQuit
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

func CWWTPEnterSulking() State {
	return CWQuit
}

func CWWTPLoadConfiguration() {
	CWACList = make([]CWACDescriptor, 1)
}

func main() {
	CWWTPLoadConfiguration()

	var nextState = CWEnterDiscovery

	for {
		switch nextState {
		case CWEnterDiscovery:
			nextState = CWWTPEnterDiscovery()
		case CWEnterSulking:
			nextState = CWWTPEnterSulking()
		case CWQuit:
			return
		}
	}
}
