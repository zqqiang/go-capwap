import React, { Component } from "react";
import TopNavigation from "./components/topNavigation.js";
import Routes from "../src/components/Routes";

class App extends Component {
  render() {
    return (
      <div className="flexible-content">
        <TopNavigation />
        <main id="content" className="p-5">
          <Routes />
        </main>
      </div>
    );
  }
}

export default App;
