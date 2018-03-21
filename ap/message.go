package main

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

// Version
const (
	Version      = 0
	CapwapHeader = 0
)

const (
	cwMsgElementDiscoveryTypeBroadcast  = 0
	cwMsgElementDiscoveryTypeConfigured = 1
)
