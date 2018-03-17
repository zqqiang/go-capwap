package main

import (
	"github.com/stretchr/testify/assert"
)

func (s *TestSuite) TestDemo() {
	var result string

	t := Testcase{
		s,
		TestOptions{
			{Key: menu["Network"], Action: Click},
		},
		QueryOptions{
			{Key: "https://www.google.ca/", Action: Navigate},
			{Key: "//input[@name='btnK']", Action: Value, Out: &result},
		},
	}

	t.Build()

	assert := assert.New(s.T())

	assert.Equal(`Google Search`, result, "should be the same.")
}
