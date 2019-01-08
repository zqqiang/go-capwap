package users

import (
	"github.com/gin-gonic/gin"
)

func UsersRegister(router *gin.RouterGroup) {
	router.POST("/login", UsersLogin)
}

func UsersLogin(c *gin.Context) {

}
