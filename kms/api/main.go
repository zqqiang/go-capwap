package main

import (
	"github.com/gin-gonic/gin"
	"github.com/zqqiang/go-capwap/kms/api/users"
)

func main() {
	r := gin.Default()

	v1 := r.Group("/api")
	users.UsersRegister(v1.Group("/users"))

	r.Run() // listen and serve on 0.0.0.0:8080
}
