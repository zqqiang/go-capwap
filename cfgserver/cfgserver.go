package main

import (
	"bufio"
	"crypto/tls"
	"fmt"
	"log"
	"net"
	"runtime"
	"strings"
)

const (
	winCert   = "D:\\cert\\local\\FortiCloud_Service.cer"
	winKey    = "D:\\cert\\local\\FortiCloud_Service.key"
	linuxCert = "/etc/cert/local/FortiCloud_Service.cer"
	linuxKey  = "/etc/cert/local/FortiCloud_Service.key"
)

func getCertKey() (string, string) {
	switch os := runtime.GOOS; os {
	case "windows":
		return winCert, winKey
	case "linux":
		return linuxCert, linuxKey
	default:
		fmt.Printf("unsupport os: %s\n", os)
		return "", ""
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	r := bufio.NewReader(conn)

	count := 0
	for {
		msg, err := r.ReadString('\n')
		if err != nil {
			log.Println(err)
			return
		}

		if strings.Compare(msg, "\r\n") == 0 {
			fmt.Printf("sent response\n")

			n, err := conn.Write([]byte("received get ip\n"))
			if err != nil {
				log.Println(n, err)
				return
			}
			return
		}

		count++
		fmt.Printf("%d. %s\n", count, msg)
	}
}

func main() {
	log.SetFlags(log.Lshortfile)

	cer, err := tls.LoadX509KeyPair(getCertKey())
	if err != nil {
		log.Println(err)
		return
	}

	config := &tls.Config{Certificates: []tls.Certificate{cer}}
	ln, err := tls.Listen("tcp", ":541", config)
	if err != nil {
		log.Println(err)
		return
	}
	defer ln.Close()

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Println(err)
			continue
		}
		go handleConnection(conn)
	}
}
