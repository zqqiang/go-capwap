import { decorate, observable, action } from "mobx";
import agent from "../agent";
import userStore from "./userStore";
import commonStore from "./commonStore";

class AuthStore {
  inProgress = false;
  errors = undefined;

  values = {
    email: "",
    password: ""
  };

  setEmail(email) {
    this.values.email = email;
  }

  login() {
    this.inProgress = true;
    this.errors = undefined;
    return agent.Auth.login(this.values.email, this.values.password)
      .then(({ user }) => commonStore.setToken(user.token))
      .then(() => userStore.pullUser())
      .catch(
        action(err => {
          this.errors =
            err.response && err.response.body && err.response.body.errors;
          throw err;
        })
      )
      .finally(
        action(() => {
          this.inProgress = false;
        })
      );
  }
}

decorate(AuthStore, {
  inProgress: observable,
  errors: observable,
  values: observable,
  setEmail: action,
  login: action
});

export default new AuthStore();
