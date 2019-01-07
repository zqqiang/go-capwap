import React from "react";
import { observer, inject } from "mobx-react";
import { withRouter } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export default inject("authStore")(
  withRouter(
    observer(
      class Home extends React.Component {
        handleClickLogout = () => {
          this.props.authStore
            .logout()
            .then(() => this.props.history.replace("/"));
        };
        render() {
          return (
            <div className="wrapper">
              <div className="main-panel ps ps--active-y">
                <nav className="navbar-absolute fixed-top navbar-transparent navbar navbar-expand-lg">
                  <div className="container-fluid">
                    <div className="navbar-wrapper">
                      <div className="navbar-toggle">
                        <button className="navbar-toggler" type="button">
                          <span className="navbar-toggler-bar bar1" />
                          <span className="navbar-toggler-bar bar2" />
                          <span className="navbar-toggler-bar bar3" />
                        </button>
                      </div>
                      <a href="/" className="navbar-brand">
                        <span className="d-none d-md-block">KMS Server</span>
                        <span className="d-block d-md-none">KMS</span>
                      </a>
                    </div>
                    <button
                      aria-controls="navigation-index"
                      aria-expanded="false"
                      aria-label="Toggle navigation"
                      className="navbar-toggler"
                      data-toggle="collapse"
                      type="button"
                    >
                      <span className="navbar-toggler-bar navbar-kebab" />
                      <span className="navbar-toggler-bar navbar-kebab" />
                      <span className="navbar-toggler-bar navbar-kebab" />
                    </button>
                    <div className="justify-content-end collapse navbar-collapse">
                      <ul className="navbar-nav">
                        <li className="nav-item">
                          <a
                            href="/"
                            className="btn-magnify nav-link"
                            onClick={this.handleClickLogout}
                          >
                            <FontAwesomeIcon icon="sign-out-alt" />
                            <p>
                              <span className="d-lg-none d-md-block">
                                Stats
                              </span>
                            </p>
                          </a>
                        </li>
                      </ul>
                    </div>
                  </div>
                </nav>
              </div>
            </div>
          );
        }
      }
    )
  )
);
