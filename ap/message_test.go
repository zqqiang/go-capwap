package main

import (
	"reflect"
	"testing"
)

type preambleTest struct {
	wirePreamble []byte
	*Preamble
}

var preambleTests = []preambleTest{
	{
		wirePreamble: []byte{
			0x00,
		},
		Preamble: &Preamble{
			Version: 0,
			Type:    0,
		},
	},
}

func TestParsePreamble(t *testing.T) {
	p := new(Preamble)
	pp := preambleTests[0].Preamble
	wp := preambleTests[0].wirePreamble
	if err := p.Parse(wp); err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(p, pp) {
		t.Fatalf("got %#v; want %#v", p, pp)
	}
}

type headerTest struct {
	wireHeader []byte
	*Header
}

var headerTests = []headerTest{
	{
		wireHeader: []byte{
			0x10, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00,
		},
		Header: &Header{
			HeaderLength:   2,
			RadioID:        1,
			WirelessBindID: 1,
			Flags: HeaderFlags{
				PayloadType:    0,
				Fragment:       0,
				LastFragment:   0,
				WirelessHeader: 0,
				RadioMacHeader: 0,
				KeepAlive:      0,
				Reserved:       0,
			},
			FragmentID:     0,
			FragmentOffset: 0,
			Reserved:       0,
		},
	},
}

func TestParseHeader(t *testing.T) {
	h := new(Header)
	hh := headerTests[0].Header
	wh := headerTests[0].wireHeader
	if err := h.Parse(wh); err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(h, hh) {
		t.Fatalf("got %#v; want %#v", h, hh)
	}
}
