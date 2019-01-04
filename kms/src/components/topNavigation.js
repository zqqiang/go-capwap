import React, { Component } from "react";
import {
  Navbar,
  NavbarBrand,
  NavbarNav,
  NavbarToggler,
  Collapse,
  NavItem,
  NavLink,
  Fa,
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem
} from "mdbreact";

class TopNavigation extends Component {
  constructor(props) {
    super(props);
    this.state = {
      collapse: false
    };
    this.onClick = this.onClick.bind(this);
    this.toggle = this.toggle.bind(this);
  }

  onClick() {
    this.setState({
      collapse: !this.state.collapse
    });
  }

  toggle() {
    this.setState({
      dropdownOpen: !this.state.dropdownOpen
    });
  }

  render() {
    return (
      <Navbar color="info-color" dark expand="md" scrolling>
        <NavbarBrand href="/">
          <strong>KMS</strong>
        </NavbarBrand>
        <NavbarToggler onClick={this.onClick} />
        <Collapse isOpen={this.state.collapse} navbar>
          <NavbarNav left>
            <NavItem>
              <NavLink to="/">Home</NavLink>
            </NavItem>
          </NavbarNav>
          <NavbarNav right>
            <NavItem>
              <NavLink className="waves-effect waves-light" to="/Settings">
                <Fa icon="gear" className="mr-1" />
                Settings
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink className="waves-effect waves-light" to="/Profile">
                <Fa icon="user" className="mr-1" />
                Profile
              </NavLink>
            </NavItem>
          </NavbarNav>
        </Collapse>
      </Navbar>
    );
  }
}

export default TopNavigation;
