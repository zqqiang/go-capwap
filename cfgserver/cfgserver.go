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

type (
	request struct {
		method string
		args   []string
		attrs  map[string]string
	}
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

func isMessageEnd(msg string) bool {
	return (strings.Compare(msg, "\r\n") == 0)
}

func handleMessageLine(req *request, line string) error {
	if strings.Contains(line, "=") {
		arr := strings.Split(line, "=")
		key := arr[0]
		val := arr[1]
		req.attrs[key] = val
	} else {
		args := strings.Split(strings.TrimRight(line, "\r\n"), " ")
		if strings.Compare(args[0], "get") == 0 {
			req.method = "get"
			req.args = args[1:]
		} else {
			return fmt.Errorf("unknow method %s", line)
		}
	}
	return nil
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	r := bufio.NewReader(conn)

	req := &request{}
	req.attrs = make(map[string]string)

	count := 0
	for {
		line, err := r.ReadString('\n')
		if err != nil {
			log.Println(err)
			return
		}

		if isMessageEnd(line) {
			fmt.Printf("received %+v\n", req)
			fmt.Printf("sent response\n")

			n, err := conn.Write([]byte("received get ip\n"))
			if err != nil {
				log.Println(n, err)
				return
			}
			return
		}

		count++

		err = handleMessageLine(req, line)
		if err != nil {
			log.Println(err)
			return
		}
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
