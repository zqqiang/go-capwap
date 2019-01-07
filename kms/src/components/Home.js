import React from "react";
import { observer, inject } from "mobx-react";
import { withRouter } from "react-router-dom";

export default inject("authStore")(
  withRouter(
    observer(
      class Home extends React.Component {
        handleClickLogout = () => {
          this.props.authStore
            .logout()
            .then(() => this.props.history.replace("/"));
        };
        render() {
          return (
            <div>
              <button onClick={this.handleClickLogout}>Logout Now!</button>
            </div>
          );
        }
      }
    )
  )
);
