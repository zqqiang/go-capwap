package main

import (
	"crypto/tls"
	"log"
)

const (
	getIP = "get ip\r\nserialno=FGT30E3U17023830\r\nmgmtid=40283279\r\nplatform=FortiGate-30E\r\nfos_ver=500\r\nbuild=1547\r\nbranch=1547\r\nmaxvdom=5\r\nfg_ip=172.16.95.47\r\nhostname=FGT30E3U17023830\r\nharddisk=no\r\nbiover=05000016\r\nmgmt_mode=normal\r\nenc_flags=0\r\nfirst_fmgid=\r\nprobe_mode=yes\r\nvdom=root\r\nintf=wan\n"
)

func main() {
	log.SetFlags(log.Lshortfile)

	conf := &tls.Config{
		InsecureSkipVerify: true,
	}

	conn, err := tls.Dial("tcp", "127.0.0.1:541", conf)
	if err != nil {
		log.Println(err)
		return
	}
	defer conn.Close()

	n, err := conn.Write([]byte(getIP))
	if err != nil {
		log.Println(n, err)
		return
	}

	buf := make([]byte, 100)
	n, err = conn.Read(buf)
	if err != nil {
		log.Println(n, err)
		return
	}

	println(string(buf[:n]))
}
