import { action, decorate } from "mobx";
import agent from "../agent";

class DeksStore {
  updateDek() {}
  createDek(dek) {
    return agent.Deks.create(dek).then(({ dek }) => {
      return dek;
    });
  }
}

decorate(DeksStore, {
  updateDek: action,
  createDek: action
});

export default new DeksStore();
