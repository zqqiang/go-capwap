package guard

import (
	"crypto/tls"
	"crypto/x509"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func httpPoll() {
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

var (
	certFile = flag.String("cert", "./cert/local/local.cer", "A PEM eoncoded certificate file.")
	keyFile  = flag.String("key", "./cert/local/local.key", "A PEM encoded private key file.")
	caFile   = flag.String("CA", "./cert/ca/ca.cer", "A PEM eoncoded CA's certificate file.")
)

func selPollRequest() {
	requestPkt := "Protocol=3.0|Command=SelectivePoll|Firmware=FMG300-FW-5.2-0708|SerialNumber=FMG-VM0000000000|Persistent=false|DataItem=00000000FDNI00000-00000.00000-0000000000*03001000OBLT00000-00000.00000-0000000000*03001000SRUL00000-00000.00000-0000000000*03001000BREG00000-00000.00000-000000000001000000BLDV00000-00000.00000-0000000000*01000000OBJL00000-00000.00000-0000000000*01000000CATL00000-00000.00000-0000000000|ContractItem=FOSVM1IKRDQY6I3C*FOSVM1LFKABGPT5F*FOSVM1RQR1YWRZ02*FOSVM1D8XBJW4Q14|AcceptDelta=1\r\n\r\n"
	servAddr := "usfds1.fortinet.com:443"

	flag.Parse()

	// Load client cert
	cert, err := tls.LoadX509KeyPair(*certFile, *keyFile)
	if err != nil {
		log.Fatal(err)
	}

	// Load CA cert
	caCert, err := ioutil.ReadFile(*caFile)
	if err != nil {
		log.Fatal(err)
	}
	caCertPool := x509.NewCertPool()
	caCertPool.AppendCertsFromPEM(caCert)

	// Setup HTTPS client
	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		RootCAs:      caCertPool,
	}
	tlsConfig.BuildNameToCertificate()

	conn, err := tls.Dial("tcp", servAddr, tlsConfig)
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	n, err := conn.Write([]byte(requestPkt))
	if err != nil {
		panic(err)
	}

	println("sent: %s\n", requestPkt)

	buf := make([]byte, 100)
	n, err = conn.Read(buf)
	if err != nil {
		panic(err)
	}

	println("recv: %s\n", string(buf[:n]))
}
