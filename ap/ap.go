package main

import (
	"bufio"
	"fmt"
	"net"
)

func main() {
	conn, err := net.Dial("tcp", "localhost:5246")
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	fmt.Fprintf(conn, "GET / HTTP/1.0\r\n\r\n")
	status, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	fmt.Printf("ap receive: %+v\n", status)
}
