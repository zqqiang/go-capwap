package main

import (
	"encoding/binary"
	"errors"
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

func (p *Preamble) Parse(b []byte) error {
	if p == nil || len(b) < PreambleLength {
		return errors.New("preamble header too short")
	}
	p.Version = int(b[0] >> 4)
	p.Type = int(b[0] & 0x0f)
	return nil
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
	b[2] |= byte((h.Flags.Fragment & 0x80) >> 7)
	b[2] |= byte((h.Flags.LastFragment & 0x40) >> 6)
	b[2] |= byte((h.Flags.WirelessHeader & 0x20) >> 5)
	b[2] |= byte((h.Flags.RadioMacHeader & 0x10) >> 4)
	b[2] |= byte((h.Flags.KeepAlive & 0x08) >> 3)
	b[2] |= byte(h.Flags.Reserved & 0x07)
	binary.BigEndian.PutUint16(b[3:5], uint16(h.FragmentID))
	binary.BigEndian.PutUint16(b[5:7], uint16(h.FragmentOffset<<3))
	b[6] |= byte(h.Reserved & 0x07)
	return b, nil
}

func (h *Header) Parse(b []byte) error {
	if h == nil || len(b) < HeaderLength {
		return errors.New("header too short")
	}
	h.HeaderLength = int(binary.BigEndian.Uint16(b[0:2]) & 0xf800 >> 11)
	h.RadioID = int((binary.BigEndian.Uint16(b[0:2]) & 0x07c0) >> 6)
	h.WirelessBindID = int((binary.BigEndian.Uint16(b[0:2]) & 0x003e) >> 1)
	h.Flags.PayloadType = int(b[1] & 0x01)
	h.Flags.Fragment = int(b[2] & 0x80)
	h.Flags.LastFragment = int(b[2] & 0x40)
	h.Flags.WirelessHeader = int(b[2] & 0x20)
	h.Flags.RadioMacHeader = int(b[2] & 0x10)
	h.Flags.KeepAlive = int(b[2] & 0x08)
	h.Flags.Reserved = int(b[2] & 0x07)
	h.FragmentID = int(binary.BigEndian.Uint16(b[3:5]))
	h.FragmentOffset = int(binary.BigEndian.Uint16(b[5:7]) & 0xfff8)
	h.Reserved = int(b[6] & 0x07)
	return nil
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
