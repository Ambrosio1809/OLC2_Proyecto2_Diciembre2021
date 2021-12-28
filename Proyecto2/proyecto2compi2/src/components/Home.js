import React from 'react';
import './Design.css'
import { withRouter } from 'react-router-dom'
import NavegacionInit from './Navbar';

class Home extends React.Component {
    render() {

        return (
            <div>
                <NavegacionInit></NavegacionInit>

                <div className="main-container col-12" align="center">
                    <h1>
                        Coronavirus Data Analysis With Machine Learning
                    </h1>
                    <h3>Seleccione la opción que necesite en el menu superior</h3>

                </div>
            </div>
        )

    }

}
export default withRouter(Home)