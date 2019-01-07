import React from "react";
import { observer, inject } from "mobx-react";
import { withRouter } from "react-router-dom";

const columns = [
  {
    label: "#",
    className: "text-center"
  },
  {
    label: "SN"
  },
  {
    label: "DEK"
  },
  {
    label: "Since",
    className: "text-center"
  },
  {
    label: "Actions",
    className: "text-right"
  }
];

const datas = [[1, "FGT60D4615007833", "XXXXXX", "2019-01-07", "action"]];

export default inject("authStore", "userStore")(
  withRouter(
    observer(
      class Content extends React.Component {
        render() {
          return (
            <div className="content">
              <div className="row">
                <div className="col-md-12">
                  <div className="card">
                    <div className="card-header">
                      <div className="row">
                        <div className="col-md-2">
                          <h4 className="card-title">DEK List</h4>
                        </div>
                        <div className="col-md-8" />
                        <div className="col-md-2">
                          <button className="btn btn-info pull-right">
                            Create New
                          </button>
                        </div>
                      </div>
                    </div>
                    <div className="card-header">
                      <div className="table-responsive">
                        <table className="table">
                          <thead className="text-primary">
                            <tr>
                              {columns.map(column => (
                                <th
                                  className={column.className}
                                  key={column.label}
                                >
                                  {column.label}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {datas.map((row, index) => (
                              <tr key={index}>
                                {row.map((item, index) => (
                                  <td
                                    className={columns[index].className}
                                    key={item}
                                  >
                                    {item}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
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
