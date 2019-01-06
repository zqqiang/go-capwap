import React from "react";
import { withRouter } from "react-router-dom";
import { inject, observer } from "mobx-react";

export default inject("authStore")(
  withRouter(
    observer(
      class TopNavigation extends React.Component {
        constructor(props) {
          super(props);
          this.state = { windowWidth: 0 };
        }

        handleClickLogout = () => {
          this.props.authStore
            .logout()
            .then(() => this.props.history.replace("/"));
        };

        render() {
          return (
            <nav
              className="navbar"
              role="navigation"
              aria-label="main navigation"
            >
              <div className="navbar-brand">
                <a className="navbar-item" href="/">
                  <span className="icon">
                    <i className="fas fa-home" />
                  </span>
                </a>
                <a
                  role="button"
                  className="navbar-burger burger"
                  aria-label="menu"
                  aria-expanded="false"
                  data-target="navbar-kms"
                  href="/"
                >
                  <span aria-hidden="true" />
                  <span aria-hidden="true" />
                  <span aria-hidden="true" />
                </a>
              </div>
              <div id="navbar-kms" className="navbar-menu">
                <div className="navbar-start">
                  <a className="navbar-item" href="/Home">
                    Home
                  </a>
                </div>
                <div className="navbar-end">
                  <div className="navbar-item has-dropdown is-hoverable">
                    <a className="navbar-link">User</a>
                    <div className="navbar-dropdown">
                      <a
                        className="navbar-item"
                        onClick={this.handleClickLogout}
                      >
                        Logout
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </nav>
          );
        }
      }
    )
  )
);
