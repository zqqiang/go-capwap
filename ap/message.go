package main

import (
	"encoding/binary"
	"fmt"
	"syscall"
)

const (
	CapwapHeader   = 0
	PreambleLength = 1
	HeaderLength   = 7
	IEEE80211      = 1
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
	b := make([]byte, PreambleLength)
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

func (h *Header) String() string {
	if h == nil {
		return "<nil>"
	}
	return fmt.Sprintf("headerLength=%d radioID=%d wirelessBindID=%d flags=%#x fragmentID=%d fragmentOffset=%d",
		h.HeaderLength, h.RadioID, h.WirelessBindID, h.Flags, h.FragmentID, h.FragmentOffset)
}

func (h *Header) Marshal() ([]byte, error) {
	if h == nil {
		return nil, syscall.EINVAL
	}
	b := make([]byte, HeaderLength)
	binary.BigEndian.PutUint16(b[0:2], uint16(h.HeaderLength<<11|h.RadioID<<6|h.WirelessBindID<<1))
	b[1] |= byte(h.Flags.PayloadType & 0x01)
	b[2] |= byte(h.Flags.Fragment & 0x80)
	b[2] |= byte(h.Flags.LastFragment & 0x40)
	b[2] |= byte(h.Flags.WirelessHeader & 0x20)
	b[2] |= byte(h.Flags.RadioMacHeader & 0x10)
	b[2] |= byte(h.Flags.KeepAlive & 0x08)
	b[2] |= byte(h.Flags.Reserved & 0x07)
	binary.BigEndian.PutUint16(b[3:5], uint16(h.FragmentID))
	binary.BigEndian.PutUint16(b[5:7], uint16(h.FragmentOffset<<3))
	b[6] |= byte(h.Reserved & 0x07)
	return b, nil
}
