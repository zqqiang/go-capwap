package main

var menu = map[string]string{
	"Network":     `//div[text()='Network']`,
	"Interfaces":  `//div[text()='Interfaces']`,
	"DNS Servers": `//div[text()='DNS Servers']`,
}

var button = map[string]string{
	"Save":        `//button/span[text()='Save']`,
	"Deploy":      `//button[text()='Deploy']`,
	"Apply":       `//button[text()='Apply']`,
	"OK":          `//button[text()='OK']`,
	"Close":       `//button/span[text()='Close']`,
	"Immediately": `//label[text()='Immediately']`,
}
