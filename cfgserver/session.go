package main

import "net"

type (
	Dev struct {
		mgmt_id int
	}

	Session struct {
		conn        net.Conn
		assigned_ip string
		dev         Dev
	}
)
