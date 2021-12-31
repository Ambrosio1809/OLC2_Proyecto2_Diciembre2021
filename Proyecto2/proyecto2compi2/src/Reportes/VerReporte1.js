import React from 'react'
import { Table } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavegacionInit from '../components/Navbar';



class VerReporte1 extends React.Component {

    state = {
        prueba: [],
        a: 0
    }

    async componentDidMount() {
        const res = await fetch(`http://localhost:4000/GetReporte1`)
        const data = await res.json();
        this.setState({ prueba: data })
        console.log(data);
    }
    render() {
        return (

            <div>
                <NavegacionInit />
                <div className="main-container col-12">
                    <h1>Reporte No.1</h1>
                    <h3>Tendencia de la infección por Covid-19 en un País</h3>
                    <Table>
                        <tbody>
                            <tr>
                                <td>
                                    {this.state.prueba.imagen ?
                                        <img width='750' height='750' src={`data:image/png;base64,${this.state.prueba.imagen}`} /> :
                                        ''}
                                </td>
                                <td>
                                    A continuación se presenta la tendencia de la infección covid-19 respecto a los casos confirmados en {this.state.prueba.pais}
                                </td>
                            </tr>


                        </tbody>
                    </Table>
                </div>
            </div>
        )
    }

}
export default VerReporte1;