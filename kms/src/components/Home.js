import React from "react";
import TopNavigation from "./TopNavigation";
import Footer from "./Footer";
import { Switch, Route } from "react-router-dom";
import Table from "./Table";

export default class Home extends React.Component {
  render() {
    return (
      <div>
        <section className="hero is-fullheight">
          <TopNavigation />
          <div className="hero-body">
            <div className="container">
              <Switch>
                <Route path="/" component={Table} />
              </Switch>
            </div>
          </div>
          <Footer />
        </section>
      </div>
    );
  }
}
