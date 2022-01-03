import React from 'react'
import { Table } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavegacionInit from '../components/Navbar';
import {Button } from 'react-bootstrap';
import {jsPDF} from 'jspdf'

class VerReporte3 extends React.Component {

    state = {
        prueba: [],
        a: 0
    }

    async componentDidMount() {
        const res = await fetch(`http://localhost:4000/GetReporte3`)
        const data = await res.json();
        this.setState({ prueba: data })
        console.log(data);
    }

    handleSubmit = async e => {
        e.preventDefault()
        var doc = new jsPDF('p', 'pt');
        doc.setFont('Arial', 'normal')
        doc.text(250,35, "Reporte No. 3")
        doc.text(125,60, `Indice de Progesión de la pandemia`)
        doc.setFontSize('15')
        doc.text(90,90,`Formula de la Regresión Lineal: ${this.state.prueba.formula} \nCon un error cuadratico (RMSE) medio de : ${this.state.prueba.RMSE} \ny un porcentaje de variación (R2) de: ${this.state.prueba.R2} \nEl indice de la pandemia es: ${this.state.prueba.coef} %\nel intercepto en el eje Y de la recta es: ${this.state.prueba.intercept}`) 
        doc.addImage(`data:image/png;base64,${this.state.prueba.imagen}`,'PNG',50,175,500,500)
        doc.setFontSize('15')
        doc.text(35,690,`Conclusión: ${this.state.prueba.Conclusion}`)
        doc.setFontSize('16')
        doc.text(35,805,"Organizacion de Lenguajes y Compiladores 2")
        doc.text(35,825,"Fernando Alberto Ambrosio Alemán                                                    201404106")
        doc.save("Reporte3.pdf")
    }

    render() {
        return (

            <div>
                <NavegacionInit />
                <div className="main-container col-12">
                    <h1>Reporte No.3</h1>
                    <h3>Indice de Progresión de la pandemia.</h3>
                    <Button variant="primary" onClick={this.handleSubmit}>
                            Download
                    </Button>
                    <Table>
                        <tbody align="center">
                            <tr>
                                <td>
                                    A continuación se presenta el Indice de Progresión de la pandemia<br></br>
                                    El cual se realizó con una regresión lineal, la cual nos presenta la siguiente formula: <br></br>{this.state.prueba.formula}<br></br>
                                    Con un error cuadratico (RMSE) medio de : {this.state.prueba.RMSE}<br></br>
                                    y un porcentaje de variación (R2) de: {this.state.prueba.R2}<br></br>
                                    El indice de la pandemia es: {this.state.prueba.coef}<br></br>
                                    el intercepto en el eje Y de la recta es: {this.state.prueba.intercept}

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
                                    {this.state.prueba.Conclusion}
                                </td>
                            </tr>


                        </tbody>
                    </Table>
                </div>
            </div>
        )
    }

}
export default VerReporte3;