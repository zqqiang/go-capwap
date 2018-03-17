package main

import (
	"github.com/chromedp/chromedp"
	"time"
)

var cloud = map[string]string{
	"url":            `https://alpha.forticloud.com`,
	"email":          `input#email`,
	"password":       `input[name='password']`,
	"login":          `input[type='submit']`,
	"FGT_SN":         `//div[text()='FGT60D4615007833']`,
	"Management_Tab": `//div[text()='Management']`,
}

var fortiGate = map[string]string{
	"url":      `http://172.16.95.49/login`,
	"username": `input#username`,
	"password": `input#secretkey`,
	"Login":    `button#login_button`,
	"Later":    `//button[text()='Later']`,
}

func cloudLogin() chromedp.Tasks {
	m := cloud
	return chromedp.Tasks{
		chromedp.Navigate(m["url"]),
		chromedp.SetValue(m["email"], `zqqiang@fortinet.com`),
		chromedp.SetValue(m["password"], `SuperCRM801`),
		chromedp.Click(m["login"]),

		chromedp.Sleep(1 * time.Second),
		chromedp.Click(m["FGT_SN"], chromedp.NodeVisible),
		chromedp.Sleep(1 * time.Second),
		chromedp.Click(m["Management_Tab"], chromedp.NodeVisible),
		chromedp.Sleep(3 * time.Second),
	}
}

func fortiGateLogin() chromedp.Tasks {
	m := fortiGate
	return chromedp.Tasks{
		chromedp.Navigate(m["url"]),
		chromedp.SetValue(m["username"], `admin`),
		chromedp.SetValue(m["password"], `admin`),
		chromedp.Click(m["Login"], chromedp.NodeVisible),
		chromedp.Sleep(1 * time.Second),
		// chromedp.Click(m["Later"], chromedp.NodeVisible),
	}
}

func saveAndDeploy() chromedp.Tasks {
	m := button
	return chromedp.Tasks{
		chromedp.Click(m["Save"], chromedp.NodeVisible),
		chromedp.Sleep(1 * time.Second),
		chromedp.Click(m["Deploy"], chromedp.NodeVisible),
		chromedp.Click(m["Immediately"], chromedp.NodeVisible),
		chromedp.Click(m["Apply"], chromedp.NodeVisible),
		chromedp.Click(m["OK"], chromedp.NodeVisible),
		chromedp.Click(m["Close"], chromedp.NodeVisible),
	}
}
