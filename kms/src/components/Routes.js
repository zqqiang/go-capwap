import React from "react";
import { Route, Switch } from "react-router-dom";
import Table from "./Table";

class Routes extends React.Component {
  render() {
    return (
      <Switch>
        <Route path="/" exact component={Table} />
      </Switch>
    );
  }
}

export default Routes;
