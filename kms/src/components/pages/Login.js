import React from "react";
import { withRouter } from "react-router-dom";
import { observer, inject } from "mobx-react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export default inject("authStore")(
  withRouter(
    observer(
      class Login extends React.Component {
        handleEmailChange = e => this.props.authStore.setEmail(e.target.value);
        handlePasswordChange = e =>
          this.props.authStore.setPassword(e.target.value);
        handleSubmitForm = e => {
          e.preventDefault();
          this.props.authStore.login().then(() => {
            this.props.history.replace("/");
          });
        };
        handleKeyPress = e => {
          if (e.key === "Enter") {
            this.handleSubmitForm(e);
          }
        };

        render() {
          const { values, errors } = this.props.authStore;

          return (
            <div className="wrapper wrapper-full-page ps">
              <div className="full-page section-image">
                <div className="login-page">
                  <div className="container">
                    <div className="row">
                      <div className="ml-auto mr-auto col-md-6 col-lg-4">
                        <form className="form">
                          <div className="card-login card">
                            <div className="card-header">
                              <div className="card-header">
                                <h3 className="header text-center">
                                  KMS Login
                                </h3>
                              </div>
                            </div>
                            <div className="card-body">
                              <div className="input-group">
                                <div className="input-group-prepend">
                                  <span className="input-group-text">
                                    <FontAwesomeIcon icon="user" />
                                  </span>
                                </div>
                                <input
                                  placeholder="Email"
                                  type="text"
                                  className="form-control"
                                  value={values.email}
                                  onChange={this.handleEmailChange}
                                />
                              </div>
                              <div className="input-group">
                                <div className="input-group-prepend">
                                  <span className="input-group-text">
                                    <FontAwesomeIcon icon="key" />
                                  </span>
                                </div>
                                <input
                                  placeholder="Password"
                                  autoComplete="off"
                                  type="password"
                                  className="form-control"
                                  value={values.password}
                                  onChange={this.handlePasswordChange}
                                  onKeyPress={this.handleKeyPress}
                                />
                              </div>
                              {errors && (
                                <div
                                  className="alert alert-danger alert-dismissible show"
                                  role="alert"
                                >
                                  {Object.keys(errors).map(key => {
                                    return (
                                      <span key={key}>
                                        <b>{key} - </b>
                                        {errors[key]}
                                      </span>
                                    );
                                  })}
                                </div>
                              )}
                            </div>
                            <div className="card-footer">
                              <a
                                href="/pages/login"
                                className="btn-round mb-3 btn btn-warning btn-block"
                                onClick={this.handleSubmitForm}
                              >
                                Get Started
                              </a>
                            </div>
                          </div>
                        </form>
                      </div>
                    </div>
                  </div>
                  <div className="full-page-background" />
                </div>
                <footer className="footer">
                  <div className="container-fluid">
                    <div className="row">
                      <div className="credits ml-auto">
                        <span className="copyright">
                          © 2019, made with <FontAwesomeIcon icon="heart" /> by
                          FortiCloud
                        </span>
                      </div>
                    </div>
                  </div>
                </footer>
              </div>
            </div>
          );
        }
      }
    )
  )
);
