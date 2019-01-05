import React from "react";
import TopNavigation from "./TopNavigation";
import Copyrights from "./Footer";
import Routes from "./Routes";

export default class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = { windowWidth: 0 };
  }
  render() {
    return (
      <div className="app">
        <div className="flexible-content white-skin">
          <TopNavigation className="white-skin" />
          <main style={{ margin: "6rem 6% 0" }}>
            <Routes />
          </main>
          <Copyrights
            style={{ position: "fixed", width: "100%" }}
            className="d-none d-lg-block"
          />
        </div>
      </div>
    );
  }
}
