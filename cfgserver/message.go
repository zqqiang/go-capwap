package main

import (
	"fmt"
)

type (
	Method int

	Message struct {
		method Method
		args   []string
		attrs  map[string]string
	}

	HandlerFunc func(*Message)
)

const (
	REPLY Method = iota
	GET
)

const (
	STATUS_OK = "200"
)

func (method Method) String() string {
	names := [...]string{
		"reply",
		"get",
	}
	return names[method]
}

func getHandler(req *Message) {
	fmt.Printf("get handler\n")

	rsp := &Message{}
	rsp.method = REPLY
	rsp.args = append(rsp.args, STATUS_OK)

	fmt.Printf("build reply: %+v\n", rsp)
}

func (req Message) handler() {
	handlers := [...]HandlerFunc{
		nil,
		getHandler,
	}
	handlers[req.method](&req)
}
