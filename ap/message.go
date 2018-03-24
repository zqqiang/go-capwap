package main

import (
	"fmt"
	"syscall"
)

const (
	CapwapHeader = 0
)

// Preamble Struct
type Preamble struct {
	Version int
	Type    int
}

func (p *Preamble) String() string {
	if p == nil {
		return "<nil>"
	}
	return fmt.Sprintf("ver=%d type=%d", p.Version, p.Type)
}

func (p *Preamble) Marshal() ([]byte, error) {
	if p == nil {
		return nil, syscall.EINVAL
	}
	b := make([]byte, 1)
	b[0] = byte(p.Version<<4 | p.Type&0x0f)
	return b, nil
}

type HeaderFlags struct {
	PayloadType    int
	Fragment       int
	LastFragment   int
	WirelessHeader int
	RadioMacHeader int
	KeepAlive      int
	Reserved       int
}

type Header struct {
	HeaderLength   int
	RadioID        int
	WirelessBindID int
	Flags          HeaderFlags
	FragmentID     int
	FragmentOffset int
	Reserved       int
}
