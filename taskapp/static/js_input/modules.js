import { Component } from 'react'
import { render } from 'react-dom'
import fetch from 'isomorphic-fetch'



class Simulation extends Component {
    constructor(props){
        super(props)
    }

    render() {
        const { simulation_id } = this.props.data
        return <h1> Simulation number: {simulation_id} </h1>
    }
}


class JobList extends Component {

    constructor(props){
        super(props)
        this.state = {
            simulations: [],
            loading: true
        }
    }

    componentDidMount() {
        this.setState({loading: true})
        this.interval = setInterval(() => {
        fetch('http://127.0.0.1:5000/api/all_jobs')
            .then(response => response.json())
            .then(simulations => 
                this.setState({simulations, loading: false}))
            }, 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }


    render() {
        const { simulations, loading } = this.state
        return ((loading) ?
            <div> Loading simulations. </div> :
            (!simulations.length) ?
                <div>No simulations.</div> :
                <ul>
                    {simulations.map((simulation, i) => <Simulation key={i} data={simulation}></Simulation>)}
                </ul>)
    }

}

export default JobList