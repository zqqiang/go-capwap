import React from "react";
import { observer, inject } from "mobx-react";
import { withRouter } from "react-router-dom";

export default inject("authStore", "userStore")(
  withRouter(
    observer(
      class Home extends React.Component {
        render() {
          return (
            <footer className="footer">
              <div className="container-fluid">
                <div className="row">
                  <div className="credits ml-auto">
                    <span className="copyright">
                      © 2019, made by FortiCloud
                    </span>
                  </div>
                </div>
              </div>
            </footer>
          );
        }
      }
    )
  )
);
