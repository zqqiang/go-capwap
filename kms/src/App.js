import React, { Component } from "react";
import { Switch, Route, withRouter } from "react-router-dom";

import TopNavigation from "./components/topNavigation.js";
import Routes from "../src/components/Routes";

import Login from "./components/pages/Login";
import { observer, inject } from "mobx-react";

import PrivateRoute from "./components/PrivateRoute";
import Home from "./components/Home";

export default inject("commonStore")(
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
            // todo
          }
        }
        render() {
          return (
            <Switch>
              <Route path="/pages/login" exact component={Login} />
              <PrivateRoute path="/" commponent={Home} />
            </Switch>
          );
        }
      }
    )
  )
);
