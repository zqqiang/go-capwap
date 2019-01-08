import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "mobx-react";

import "bootstrap/dist/css/bootstrap.css";
import "./assets/scss/main.scss";

import App from "./App";
import * as serviceWorker from "./serviceWorker";
import { BrowserRouter as Router } from "react-router-dom";

import commonStore from "./stores/commonStore";
import userStore from "./stores/userStore";
import authStore from "./stores/authStore";
import editorStore from "./stores/editorStore";

import { library } from "@fortawesome/fontawesome-svg-core";
import { fab } from "@fortawesome/free-brands-svg-icons";
import {
  faUser,
  faKey,
  faHeart,
  faSignOutAlt
} from "@fortawesome/free-solid-svg-icons";

library.add(fab, faUser, faKey, faHeart, faSignOutAlt);

const stores = {
  commonStore,
  userStore,
  authStore,
  editorStore
};

ReactDOM.render(
  <Provider {...stores}>
    <Router>
      <App />
    </Router>
  </Provider>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
