import React from "react";
import { withRouter } from "react-router-dom";
import { observer, inject } from "mobx-react";

import "./Login.css";

export default inject("authStore")(
  withRouter(
    observer(
      class Login extends React.Component {
        handleEmailChange = e => this.props.authStore.setEmail(e.target.value);
        handlePasswordChange = e =>
          this.props.authStore.setPassword(e.target.value);
        handleSubmitForm = e => {
          e.preventDefault();
          this.props.authStore.login().then(() => {
            this.props.history.replace("/");
          });
        };
        handleKeyPress = e => {
          if (e.key === "Enter") {
            this.handleSubmitForm(e);
          }
        };

        render() {
          const { values, errors } = this.props.authStore;

          return <div>Login Page</div>;
        }
      }
    )
  )
);
