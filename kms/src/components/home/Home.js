import React from "react";
import { Route } from "react-router-dom";

import Navbar from "./Navbar";
import Footer from "./Footer";
import Content from "./Content";
import Edit from "../pages/Editor";

class Home extends React.Component {
  handleClickLogout = () => {
    this.props.authStore.logout().then(() => this.props.history.replace("/"));
  };
  render() {
    return (
      <div className="wrapper">
        <div className="main-panel ps ps--active-y">
          <Navbar />
          <div className="content">
            <Route path="/" exact component={Content} />
            <Route path="/Edit" exact component={Edit} />
          </div>
          <Footer />
        </div>
      </div>
    );
  }
}

export default Home;
