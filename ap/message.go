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

const (
	ControlHeaderLength = 8
)

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

type MessageType struct {
	EnterpriseNumber   int
	EnterpriseSpecific int
}

func (m *MessageType) String() string {
	if m == nil {
		return "<nil>"
	}
	return fmt.Sprintf("enterpriseNumber=%d enterpriseSpecific=%d",
		m.EnterpriseNumber, m.EnterpriseSpecific)
}

type ControlHeader struct {
	MessageType          MessageType
	SequenceNumber       int
	MessageElementLength int
	Flags                int
}

func (c *ControlHeader) String() string {
	if c == nil {
		return "<nil>"
	}
	return fmt.Sprintf("messageType=[%s] sequenceNumber=%d messageElementLegnth=%d flags=%#x",
		c.MessageType.String(), c.SequenceNumber, c.MessageElementLength, c.Flags)
}

func (c *ControlHeader) Marshal() ([]byte, error) {
	if c == nil {
		return nil, syscall.EINVAL
	}
	b := make([]byte, ControlHeaderLength)
	binary.BigEndian.PutUint32(b[0:4], uint32(c.MessageType.EnterpriseNumber<<8|c.MessageType.EnterpriseSpecific&0x000f))
	b[4] = byte(c.SequenceNumber)
	binary.BigEndian.PutUint16(b[5:7], uint16(c.MessageElementLength))
	b[7] = byte(c.Flags)
	return b, nil
}
