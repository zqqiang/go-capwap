package guard

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func poll() {
	rs, err := http.Get("https://google.com")
	if err != nil {
		panic(err)
	}
	defer rs.Body.Close()

	bodyBytes, err := ioutil.ReadAll(rs.Body)
	if err != nil {
		panic(err)
	}

	bodyString := string(bodyBytes)

	fmt.Println(bodyString)
}
