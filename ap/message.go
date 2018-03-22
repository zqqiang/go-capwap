package main

// Preamble Struct
type Preamble struct {
	preamble uint8
}

func (p *Preamble) setVersion(version uint8) {
	p.preamble |= version << 4
}

const (
	capwapHeader = 0
)

func (p *Preamble) setType(preambleType uint8) {
	p.preamble |= (preambleType & 0x0f)
}

// Header Struct
type Header struct {
	part1      [3]uint8
	fragmentID uint16
	part3      uint16
}

func (h *Header) setHeaderLength(length uint8) {
	h.part1[0] |= length << 5
}

type discoveryRequest struct {
	preamble      Preamble
	discoveryType uint8
}

const (
	cwMsgElementDiscoveryTypeBroadcast  = 0
	cwMsgElementDiscoveryTypeConfigured = 1
)
