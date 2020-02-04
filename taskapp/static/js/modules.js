var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import { Component } from 'react';
import { render } from 'react-dom';
import fetch from 'isomorphic-fetch';

var Simulation = function (_Component) {
    _inherits(Simulation, _Component);

    function Simulation(props) {
        _classCallCheck(this, Simulation);

        return _possibleConstructorReturn(this, (Simulation.__proto__ || Object.getPrototypeOf(Simulation)).call(this, props));
    }

    _createClass(Simulation, [{
        key: 'render',
        value: function render() {
            var simulation_id = this.props.data.simulation_id;

            return React.createElement(
                'h1',
                null,
                ' Simulation number: ',
                simulation_id,
                ' '
            );
        }
    }]);

    return Simulation;
}(Component);

var JobList = function (_Component2) {
    _inherits(JobList, _Component2);

    function JobList(props) {
        _classCallCheck(this, JobList);

        var _this2 = _possibleConstructorReturn(this, (JobList.__proto__ || Object.getPrototypeOf(JobList)).call(this, props));

        _this2.state = {
            simulations: [],
            loading: true
        };
        return _this2;
    }

    _createClass(JobList, [{
        key: 'componentDidMount',
        value: function componentDidMount() {
            var _this3 = this;

            this.setState({ loading: true });
            this.interval = setInterval(function () {
                fetch('http://127.0.0.1:5000/api/all_jobs').then(function (response) {
                    return response.json();
                }).then(function (simulations) {
                    return _this3.setState({ simulations: simulations, loading: false });
                });
            }, 1000);
        }
    }, {
        key: 'componentWillUnmount',
        value: function componentWillUnmount() {
            clearInterval(this.interval);
        }
    }, {
        key: 'render',
        value: function render() {
            var _state = this.state,
                simulations = _state.simulations,
                loading = _state.loading;

            return loading ? React.createElement(
                'div',
                null,
                ' Loading simulations. '
            ) : !simulations.length ? React.createElement(
                'div',
                null,
                'No simulations.'
            ) : React.createElement(
                'ul',
                null,
                simulations.map(function (simulation, i) {
                    return React.createElement(Simulation, { key: i, data: simulation });
                })
            );
        }
    }]);

    return JobList;
}(Component);

export default JobList;