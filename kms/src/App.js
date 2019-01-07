import React, { Component } from "react";

import { Switch, Route, withRouter } from "react-router-dom";
import { observer, inject } from "mobx-react";

import Login from "./components/pages/Login";
import PrivateRoute from "./components/PrivateRoute";
import Home from "./components/Home";

export default inject("commonStore", "userStore")(
  withRouter(
    observer(
      class App extends Component {
        componentWillMount() {
          if (!this.props.commonStore.token) {
            this.props.commonStore.setAppLoaded();
          }
        }
        componentDidMount() {
          if (this.props.commonStore.token) {
            this.props.userStore
              .pullUser()
              .finally(() => this.props.commonStore.setAppLoaded());
          }
        }
        render() {
          if (this.props.commonStore.appLoaded) {
            return (
              <Switch>
                <Route path="/pages/login" exact component={Login} />
                <PrivateRoute path="/" component={Home} />
              </Switch>
            );
          }
          return <div>App loading...</div>;
        }
      }
    )
  )
);
