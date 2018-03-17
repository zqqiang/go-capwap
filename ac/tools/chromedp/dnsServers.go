package main

import (
	"github.com/stretchr/testify/assert"
)

var cloudDnsServers = map[string]string{
	"Create New for DNS Service":  `(//button[text()='Create New'])[1]`,
	"Create New for DNS Database": `(//button[text()='Create New'])[2]`,
	"Delete dmz":                  `(//div[@title='Delete'])[1]`,

	"Interface Select":   `(//div[@class='short-select'])[1]`,
	"Interface wan1":     `//div[text()='wan1']`,
	"Mode Select":        `(//div[@class='short-select'])[2]`,
	"Mode Non Recursive": `//div[text()='NON_RECURSIVE']`,
}

var fgtDnsServers = map[string]string{
	"dmzUrl":    `http://172.16.95.49/ng/network/dns/service/edit/dmz`,
	"wan1Url":   `http://172.16.95.49/ng/network/dns/service/edit/wan1`,
	"Interface": `//*[@id="ng-base"]/form/div[2]/div[2]/section/f-field[1]/div/field-value/div/div/div[1]/div/span/span/span`,
	"Mode":      `input:checked`,

	"dnsServersUrl":            `http://172.16.95.49/ng/network/dns`,
	"DNS Service on Interface": `//*[@id="navbar-view-section"]/div/f-dns-servers/div/section[1]/f-dns-service-list/f-list/div/div[2]/div[1]/div[2]/table/tbody/tr/td`,
}

func (s *TestSuite) TestDnsServersCreate() {
	var inter string
	var mode string

	t := Testcase{
		s,
		TestOptions{
			{Key: menu["Network"], Action: Click},
			{Key: menu["DNS Servers"], Action: Click},
			{Key: menu["Create New for DNS Service"], Action: Click}, // todo: some error
		},
		QueryOptions{
			{Key: fgtDnsServers["dmzUrl"], Action: Navigate},
			{Key: fgtDnsServers["Interface"], Action: Text, Out: &inter},
			{Key: fgtDnsServers["Mode"], Action: Value, Out: &mode},
		},
	}

	t.Build()

	assert := assert.New(s.T())

	assert.Equal(`dmz`, inter, "should be the same.")
	assert.Equal(`recursive`, mode, "should be the same.")
}

func (s *TestSuite) TestDnsServersDelete() {
	var inter string

	t := Testcase{
		s,
		TestOptions{
			{Key: menu["Network"], Action: Click},
			{Key: menu["DNS Servers"], Action: Click},
			{Key: menu["Delete dmz"], Action: Click},
		},
		QueryOptions{
			{Key: fgtDnsServers["dnsServersUrl"], Action: Navigate},
			{Key: fgtDnsServers["DNS Service on Interface"], Action: Text, Out: &inter},
		},
	}

	t.Build()

	assert := assert.New(s.T())

	assert.Equal(`No matching entries found`, inter, "should be the same.")
}

func (s *TestSuite) TestDnsServersCreateWan1() {
	var inter string
	var mode string

	t := Testcase{
		s,
		TestOptions{
			{Key: menu["Network"], Action: Click},
			{Key: menu["DNS Servers"], Action: Click},
			{Key: menu["Create New for DNS Service"], Action: Click},
			{Key: menu["Interface Select"], Action: Click},
			{Key: menu["Interface wan1"], Action: Click},
			{Action: Sleep},
			{Key: menu["Mode Select"], Action: Click},
			{Key: menu["Mode Non Recursive"], Action: Click},
		},
		QueryOptions{
			{Key: fgtDnsServers["wan1Url"], Action: Navigate},
			{Key: fgtDnsServers["Interface"], Action: Text, Out: &inter},
			{Key: fgtDnsServers["Mode"], Action: Value, Out: &mode},
		},
	}

	t.Build()

	assert := assert.New(s.T())

	assert.Equal(`wan1`, inter, "should be the same.")
	assert.Equal(`non-recursive`, mode, "should be the same.")
}
