package main

import (
	"context"
	"github.com/chromedp/chromedp"
	"github.com/chromedp/chromedp/runner"
	"github.com/stretchr/testify/suite"
	"log"
	"testing"
)

type TestSuite struct {
	suite.Suite
	ctxt   context.Context
	c      *chromedp.CDP
	cancel context.CancelFunc
}

func (s *TestSuite) SetupSuite() {
	var err error

	// create context
	s.ctxt, s.cancel = context.WithCancel(context.Background())

	// create chrome instance
	s.c, err = chromedp.New(
		s.ctxt,
		chromedp.WithRunnerOptions(
			// runner.Flag("headless", true),
			runner.Flag("no-sandbox", true),
			runner.WindowSize(1920, 1080),
		),
		chromedp.WithLog(log.Printf),
	)
	if err != nil {
		log.Fatal(err)
	}
}

func (s *TestSuite) TearDownSuite() {
	var err error
	defer s.cancel()

	// shutdown chrome
	err = s.c.Shutdown(s.ctxt)
	if err != nil {
		log.Fatal(err)
	}

	// wait for chrome to finish
	err = s.c.Wait()
	if err != nil {
		log.Fatal(err)
	}
}

func (s *TestSuite) SetupTest() {
	log.Print("SetupTest")
}

func (s *TestSuite) TearDownTest() {
	log.Print("TearDownTest")
}

// In order for 'go test' to run this suite, we need to create
// a normal test function and pass our suite to suite.Run
func TestChromedpTestSuite(t *testing.T) {
	suite.Run(t, new(TestSuite))
}
