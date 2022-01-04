import React from 'react'
import { Table } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavegacionInit from '../components/Navbar';
import {Button } from 'react-bootstrap';
import {jsPDF} from 'jspdf'

class VerReporte25 extends React.Component {

    state = {
        prueba: [],
        a: 0
    }

    async componentDidMount() {
        const res = await fetch(`http://3.16.160.225:4000/GetReporte25`)
        const data = await res.json();
        this.setState({ prueba: data })
        console.log(data);
    }

    handleSubmit = async e => {
        e.preventDefault()
        var doc = new jsPDF('p', 'pt');
        doc.setFont('Arial', 'normal')
        doc.text(250,35, "Reporte No. 25")
        doc.text(165,60, `Predicción de casos confirmados por día`)
        doc.setFontSize('15')
        doc.text(60,95,`Para una cantidad de ${this.state.prueba.Dias} dias se tiene un resultado aproximado de: ${this.state.prueba.prediccion} casos\nEl cual se realizó con una regresión polinomial de grado ${this.state.prueba.grado}\nCon un error cuadratico (RMSE) medio de : ${this.state.prueba.RMSE}\ny un porcentaje de variación (R2) de: ${this.state.prueba.R2}`) 
        doc.addImage(`data:image/png;base64,${this.state.prueba.imagen}`,'PNG',50,175,500,500)
        doc.setFontSize('15')
        doc.text(35,690,`Conclusión: ${this.state.prueba.Conclusion}`)
        doc.setFontSize('16')
        doc.text(35,805,"Organizacion de Lenguajes y Compiladores 2")
        doc.text(35,825,"Fernando Alberto Ambrosio Alemán                                                    201404106")
        doc.save("Reporte25.pdf")
    }
    
    render() {
        return (

            <div>
                <NavegacionInit />
                <div className="main-container col-12">
                    <h1>Reporte No.25</h1>
                    <h3>Predicción de casos confirmados por día</h3>
                    <Button variant="primary" onClick={this.handleSubmit}>
                            Download
                    </Button>
                    <Table>
                        <tbody align="center">
                            <tr>
                                <td>
                                    A continuación se presenta la Predicción de casos confirmados por día mundialmente<br></br>
                                    Para una cantidad de {this.state.prueba.Dias} dias se tiene un resultado aproximado de: {this.state.prueba.prediccion} casos<br></br>
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
export default VerReporte25;