import { observable, action, decorate, reaction } from "mobx";

class CommonStore {
  appName = "KMS";
  token = window.localStorage.getItem("jwt");
  appLoaded = false;

  constructor() {
    reaction(
      () => this.token,
      token => {
        if (token) {
          window.localStorage.setItem("jwt", token);
        } else {
          window.localStorage.removeItem("jwt");
        }
      }
    );
  }

  setToken(token) {
    this.token = token;
  }

  setAppLoaded() {
    this.appLoaded = true;
  }
}

decorate(CommonStore, {
  appName: observable,
  token: observable,
  appLoaded: observable,
  setToken: action,
  setAppLoaded: action
});

export default new CommonStore();
