package main

type (
	Method int

	Request struct {
		method Method
		args   []string
		attrs  map[string]string
	}
)

const (
	GET Method = iota
)

func (method Method) String() string {
	names := [...]string{
		"get",
	}
	return names[method]
}
