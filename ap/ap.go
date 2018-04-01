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
	address  string
	received bool
	seqNum   int
}

var CWACList []CWACDescriptor

var seqNum int

const (
	MaxSeqNum = 255
)

func CWGetSeqNum() int {
	if seqNum == MaxSeqNum {
		seqNum = 0
	} else {
		seqNum++
	}
	return seqNum
}

func CWAssembleDiscoveryRequest(seqNum int) ([]byte, error) {
	p := Preamble{0, CapwapHeader}
	pb, err := p.Marshal()
	if err != nil {
		return nil, err
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
		return nil, err
	}
	fmt.Printf("%s raw[% x]\n", h.String(), hb)

	c := ControlHeader{
		MessageType{0, 1},
		seqNum,
		351,
		0,
	}
	cb, err := c.Marshal()
	if err != nil {
		return nil, err
	}
	fmt.Printf("%s raw[% x]\n", c.String(), cb)

	s := append(pb, hb...)
	s = append(s, cb...)

	return s, nil
}

const (
	WtpPortControl string = "5246"
)

func CWNetworkSendUnsafeUnconnected(addr string, b []byte) error {
	conn, err := net.Dial("tcp", addr+":"+WtpPortControl)
	if err != nil {
		return err
	}
	n, err := conn.Write(b)
	if err != nil {
		return err
	}
	fmt.Printf("ap send: len %d raw[% x]\n", n, b)

	var reply = make([]byte, 1024)
	rn, err := conn.Read(reply)
	if err != nil {
		return err
	}
	fmt.Printf("ap recv: len %d raw[% x]\n", rn, reply[:rn])
	return nil
}

func CWWTPEnterDiscovery() State {
	fmt.Println("######### Discovery State #########")

	CWDiscoveryCount := 0

	for {
		if CWDiscoveryCount == CWMaxDiscoveries {
			return CWEnterSulking
		}
		for i := 0; i < len(CWACList); i++ {
			if CWACList[i].received != true {
				CWACList[0].seqNum = CWGetSeqNum()
				s, err := CWAssembleDiscoveryRequest(CWACList[0].seqNum)
				if err != nil {
					panic(err)
				}
				if err := CWNetworkSendUnsafeUnconnected(CWACList[0].address, s); err != nil {
					panic(err)
				}
			}
		}

		CWDiscoveryCount++

		fmt.Printf("WTP Discovery-To-Discovery (%d)", CWDiscoveryCount)

		break
	}

	return CWQuit
}

func CWWTPEnterSulking() State {
	return CWQuit
}

func CWWTPLoadConfiguration() {
	fmt.Println("WTP Loads Configuration")

	CWACList = make([]CWACDescriptor, 1)

	CWACList[0].address = "localhost"
	CWACList[0].received = false
	CWACList[0].seqNum = 0
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
