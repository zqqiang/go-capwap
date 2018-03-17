package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

var key string
var Map = make(map[string]int)

func buildSupp(s string) {
	if !(strings.HasPrefix(s, "==") || strings.HasPrefix(s, "--")) {
		if strings.HasPrefix(s, "{") {
			key = ""
		} else if strings.HasPrefix(s, "}") {
			if _, ok := Map[key]; ok {
				Map[key]++
			} else {
				Map[key] = 1
			}
		} else {
			if !strings.HasPrefix(s, "   <") {
				key += (s + "\n")
			}
		}
	}
}

func main() {
	file, err := os.Open("C:\\Users\\ZhaoqingQiang\\Downloads\\valgrind.log")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		buildSupp(scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	for k, v := range Map {
		fmt.Println("{")
		fmt.Println(k)
		fmt.Println("}")
		fmt.Println("used_suppression: ", v)
		fmt.Println("\n")
	}
}
