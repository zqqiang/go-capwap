import React from "react";
import {
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarNav,
  MDBIcon,
  MDBDropdown,
  MDBDropdownToggle,
  MDBDropdownMenu,
  MDBDropdownItem,
  MDBBadge
} from "mdbreact";

import { withRouter } from "react-router-dom";
import { observer, inject } from "mobx-react";

export default inject("userStore", "authStore")(
  withRouter(
    observer(
      class TopNavigation extends React.Component {
        handleClickLogout = () => {
          this.props.authStore
            .logout()
            .then(() => this.props.history.replace("/"));
        };
        render() {
          const navStyle = {
            paddingLeft: "16px",
            transition: "padding-left .3s"
          };
          return (
            <MDBNavbar
              className="flexible-MDBNavbar"
              light
              expand="md"
              scrolling
              fixed="top"
              style={{ zIndex: 3 }}
            >
              <MDBNavbarBrand href="/" style={navStyle}>
                <strong>KMS</strong>
              </MDBNavbarBrand>
              <MDBNavbarNav expand="sm" right style={{ flexDirection: "row" }}>
                <MDBDropdown>
                  <MDBDropdownToggle nav caret>
                    <MDBBadge color="red" className="mr-2">
                      1
                    </MDBBadge>
                    <MDBIcon icon="bell" />{" "}
                    <span className="d-none d-md-inline">Notifications</span>
                  </MDBDropdownToggle>
                  <MDBDropdownMenu right style={{ minWidth: "400px" }}>
                    <MDBDropdownItem href="#!">
                      <MDBIcon icon="user-secret" className="mr-2" />
                      token create
                      <span className="float-right">
                        <MDBIcon icon="clock-o" /> 13 min
                      </span>
                    </MDBDropdownItem>
                  </MDBDropdownMenu>
                </MDBDropdown>
                <MDBDropdown>
                  <MDBDropdownToggle nav caret>
                    <MDBIcon icon="user" />{" "}
                    <span className="d-none d-md-inline">User</span>
                  </MDBDropdownToggle>
                  <MDBDropdownMenu right style={{ minWidth: "200px" }}>
                    <MDBDropdownItem onClick={this.handleClickLogout}>
                      Log Out
                    </MDBDropdownItem>
                  </MDBDropdownMenu>
                </MDBDropdown>
              </MDBNavbarNav>
            </MDBNavbar>
          );
        }
      }
    )
  )
);
