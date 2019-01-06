import React from "react";

export default class Footer extends React.Component {
  render() {
    return (
      <footer className="footer">
        <div className="content has-text-centered">
          <p>
            <strong>KMS</strong> by{" "}
            <a href="https://www.forticloud.com">FortiCloud</a>.
          </p>
        </div>
      </footer>
    );
  }
}
