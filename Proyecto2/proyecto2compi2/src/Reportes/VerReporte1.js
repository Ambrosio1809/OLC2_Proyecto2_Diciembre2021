import React from 'react'
import { Table } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavegacionInit from '../components/Navbar';
import {jsPDF} from 'jspdf'
import {Button } from 'react-bootstrap';



class VerReporte1 extends React.Component {

    state = {
        prueba: [],
        a: 0
    }

    handleSubmit = async e => {
        e.preventDefault()
        var doc = new jsPDF('p', 'pt');
        doc.setFont('Arial', 'normal')
        doc.text(250,35, "Reporte No. 1")
        doc.text(125,60, `Tendencia de la infección por Covid-19 en ${this.state.prueba.pais}`)
        doc.setFontSize('15')
        doc.text(100,115,`Este reporte se realizó con una regresión polinomial de grado ${this.state.prueba.grado} \n Con un error cuadratico (RMSE) medio de : ${this.state.prueba.RMSE} \n y un porcentaje de variación (R2) de: ${this.state.prueba.R2}`) 
        doc.addImage(`data:image/png;base64,${this.state.prueba.imagen}`,'PNG',50,175,500,500)
        doc.setFontSize('15')
        doc.text(35,690,`Conclusión: ${this.state.prueba.conclusion}`)
        doc.setFontSize('16')
        doc.text(35,805,"Organizacion de Lenguajes y Compiladores 2")
        doc.text(35,825,"Fernando Alberto Ambrosio Alemán                                                    201404106")
        doc.save("Reporte1.pdf")
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
                    <Button variant="primary" onClick={this.handleSubmit}>
                            Download
                    </Button>
                    <Table>
                        <tbody align="center">
                            <tr>
                                <td>
                                    A continuación se presenta la tendencia de la infección covid-19 respecto a los casos confirmados en {this.state.prueba.pais}<br></br>
                                    El cual se realizó con una regresión polinomial de grado {this.state.prueba.grado}<br></br>
                                    Con un error cuadratico (RMSE) medio de : {this.state.prueba.RMSE}<br></br>
                                    y un porcentaje de variación (R2) de: {this.state.prueba.R2}<br></br>

                                </td>
                            </tr>
                            <tr>
                                <td>
                                    {this.state.prueba.imagen ?
                                        <img width='750' height='750' src={`data:image/png;base64,${this.state.prueba.imagen}`} /> :
                                        ''}
                                </td>

                            </tr>
                            <tr>
                                <td>

                                    <h4>
                                        Conclusion
                                    </h4>

                                </td>
                            </tr>
                            <tr>
                                <td>
                                    {this.state.prueba.conclusion}
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