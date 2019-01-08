import React from "react";
import { observer, inject } from "mobx-react";
import { withRouter } from "react-router-dom";

export default inject("editorStore")(
  withRouter(
    observer(
      class Edit extends React.Component {
        changeSerialNumber = e => {
          this.props.editorStore.setSerialNumber(e.target.value);
        };
        changeUrl = e => {
          this.props.editorStore.setUrl(e.target.value);
        };
        submitForm = ev => {
          ev.preventDefault();
          const { editorStore } = this.props;
          editorStore.submit().then(article => {
            this.props.history.replace("/");
          });
        };

        render() {
          const { serialNumber, url } = this.props.editorStore;

          return (
            <div className="row">
              <div className="col-md-6">
                <div className="card">
                  <div className="card-header">
                    <h4 className="card-title">Create New DEK</h4>
                  </div>
                  <div className="card-body">
                    <form action="#" method="#" className="">
                      <label>Serial Number</label>
                      <div className="position-relative form-group">
                        <input
                          placeholder="Serial Number"
                          type="text"
                          className="form-control"
                          value={serialNumber}
                          onChange={this.changeSerialNumber}
                        />
                      </div>
                      <label>Resource URL</label>
                      <div className="position-relative form-group">
                        <input
                          placeholder="Resource URL"
                          type="text"
                          className="form-control"
                          value={url}
                          onChange={this.changeUrl}
                        />
                      </div>
                    </form>
                  </div>
                  <div className="card-footer">
                    <button
                      type="submit"
                      className="btn-round btn btn-info"
                      onClick={this.submitForm}
                    >
                      Submit
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        }
      }
    )
  )
);
