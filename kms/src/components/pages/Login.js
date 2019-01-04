import React from "react";
import { withRouter } from "react-router-dom";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBInput,
  MDBBtn,
  MDBView,
  MDBCard,
  MDBCardBody,
  MDBMask,
  MDBIcon,
  MDBAlert
} from "mdbreact";
import "./Login.css";
import { observer, inject } from "mobx-react";

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
          const { values, errors, inProgress } = this.props.authStore;

          return (
            <div id="landing">
              <section id="home">
                <MDBView>
                  <MDBMask
                    className="d-flex justify-content-center align-items-center"
                    overlay="gradient"
                  >
                    <MDBContainer className="h-100 d-flex justify-content-center align-items-center">
                      <MDBRow className="flex-center">
                        <MDBCol
                          md="6"
                          className="text-center text-md-left mb-5"
                        >
                          <div className="white-text">
                            <h1
                              className="h1-responsive font-weight-bold wow fadeInLeft"
                              data-wow-delay="0.3s"
                            >
                              KMS System{" "}
                            </h1>
                            <hr
                              className="hr-light wow fadeInLeft"
                              data-wow-delay="0.3s"
                            />
                            <h6
                              className="wow fadeInLeft"
                              data-wow-delay="0.3s"
                            >
                              Secure, store and tightly control access to
                              tokens, passwords, certificates, encryption keys
                              for protecting secrets and other sensitive data
                              using a UI, or HTTPs API. KMS enables fine grained
                              authorization of which users and applications are
                              permitted access to secrets and keys
                            </h6>
                            <br />
                          </div>
                        </MDBCol>

                        <MDBCol md="6" className="col-xl-5 offset-xl-1">
                          <MDBCard>
                            <MDBCardBody>
                              <div className="text-center">
                                <h3 className="white-text">
                                  <MDBIcon icon="user white-text" /> Login
                                </h3>
                                <hr className="hr-light" />
                              </div>

                              <MDBInput
                                label="Your email"
                                icon="envelope"
                                type="email"
                                labelClass="white-text"
                                iconClass="white-text"
                                value={values.email}
                                onChange={this.handleEmailChange}
                              />

                              <MDBInput
                                label="Your password"
                                icon="lock"
                                type="password"
                                labelClass="white-text"
                                iconClass="white-text"
                                value={values.password}
                                onChange={this.handlePasswordChange}
                                onKeyPress={this.handleKeyPress}
                              />

                              {errors &&
                                Object.keys(errors).map(key => {
                                  return (
                                    <MDBAlert color="danger" key={key}>
                                      {key} {errors[key]}
                                    </MDBAlert>
                                  );
                                })}

                              <div className="text-center mt-4">
                                <MDBBtn
                                  color="light-blue"
                                  rounded
                                  onClick={this.handleSubmitForm}
                                >
                                  Sign in
                                </MDBBtn>
                              </div>
                            </MDBCardBody>
                          </MDBCard>
                        </MDBCol>
                      </MDBRow>
                    </MDBContainer>
                  </MDBMask>
                </MDBView>
              </section>
            </div>
          );
        }
      }
    )
  )
);
