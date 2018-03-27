package main

import (
	"reflect"
	"testing"
)

type headerTest struct {
	wirePreamble []byte
	*Preamble
}

var headerTests = []headerTest{
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
	pp := headerTests[0].Preamble
	wp := headerTests[0].wirePreamble
	if err := p.Parse(wp); err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(p, pp) {
		t.Fatalf("got %#v; want %#v", p, pp)
	}
}
