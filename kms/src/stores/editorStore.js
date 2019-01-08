import { observable, action, decorate } from "mobx";
import deksStore from "./deksStore";

class EditorStore {
  inProgress = false;
  errors = undefined;
  dekId = undefined;

  serialNumber = "";
  url = "";

  setSerialNumber(sn) {
    this.serialNumber = sn;
  }

  setUrl(url) {
    this.url = url;
  }

  submit() {
    this.inProgress = true;
    this.errors = undefined;

    const dek = {
      serialNumber: this.serialNumber,
      url: this.url
    };

    return (this.dekId ? deksStore.updateDek(dek) : deksStore.createDek(dek))
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

decorate(EditorStore, {
  inProgress: observable,
  errors: observable,
  dekId: observable,
  serialNumber: observable,
  url: observable,
  setSerialNumber: action,
  setUrl: action,
  submit: action
});

export default new EditorStore();
