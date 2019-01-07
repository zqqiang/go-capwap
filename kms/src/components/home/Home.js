import React from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";
import Content from "./Content";

class Home extends React.Component {
  handleClickLogout = () => {
    this.props.authStore.logout().then(() => this.props.history.replace("/"));
  };
  render() {
    return (
      <div className="wrapper">
        <div className="main-panel ps ps--active-y">
          <Navbar />
          <Content />
          <Footer />
        </div>
      </div>
    );
  }
}

export default Home;
