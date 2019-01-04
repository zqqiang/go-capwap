import React from "react";
import { inject, observer } from "mobx-react";
import { Route, Redirect } from "react-router-dom";

export default inject("userStore")(
  observer(
    class PrivateRoute extends React.Component {
      render() {
        const { userStore, ...restProps } = this.props;
        if (userStore.currentUser) {
          return <Route {...restProps} />;
        } else {
          return <Redirect to="/pages/login" />;
        }
      }
    }
  )
);
