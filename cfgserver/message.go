package main

import (
	"fmt"
	"log"
	"strconv"
)

type (
	Method int

	Message struct {
		method Method
		args   []string
		attrs  map[string]string
	}

	HandlerFunc func(*Message, *Session)
)

const (
	REPLY Method = iota
	GET
)

const (
	STATUS_OK = "200"

	ATTR_IP         = "ip"
	ATTR_REQUEST    = "request"
	ATTR_MGMTID     = "mgmtid"
	ATTR_REG_STATUS = "register_status"
)

func (method Method) String() string {
	names := [...]string{
		"reply",
		"get",
	}
	return names[method]
}

func getHandler(req *Message, session *Session) {
	fmt.Printf("get handler\n")

	rsp := &Message{}
	rsp.attrs = make(map[string]string)

	rsp.method = REPLY
	rsp.args = append(rsp.args, STATUS_OK)

	rsp.attrs[ATTR_REQUEST] = ATTR_IP
	rsp.attrs[ATTR_IP] = session.assigned_ip
	rsp.attrs[ATTR_MGMTID] = strconv.Itoa(session.dev.mgmt_id)
	rsp.attrs[ATTR_REG_STATUS] = "1"

	fmt.Printf("build reply: %+v\n", rsp)

	n, err := session.conn.Write([]byte("received get ip\n"))
	if err != nil {
		log.Println(n, err)
		return
	}
}

func (req Message) handler(session *Session) {
	handlers := [...]HandlerFunc{
		nil,
		getHandler,
	}
	handlers[req.method](&req, session)
}
