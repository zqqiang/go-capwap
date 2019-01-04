import { observable, action, decorate } from "mobx";
import agent from "../agent";

class UserStore {
  currentUser;
  loadingUser;

  pullUser() {
    this.loadingUser = true;
    return agent.Auth.current()
      .then(
        action(({ user }) => {
          this.currentUser = user;
        })
      )
      .finally(
        action(() => {
          this.loadingUser = false;
        })
      );
  }

  forgetUser() {
    this.currentUser = undefined;
  }
}

decorate(UserStore, {
  currentUser: observable,
  loadingUser: observable,
  pullUser: action,
  forgetUser: action
});

export default new UserStore();
