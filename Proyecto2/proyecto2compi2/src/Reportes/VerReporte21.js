import React from 'react'
import { Table } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavegacionInit from '../components/Navbar';
import {Button } from 'react-bootstrap';
import {jsPDF} from 'jspdf'

class VerReporte21 extends React.Component {

    state = {
        prueba: [],
        a: 0
    }

    async componentDidMount() {
        const res = await fetch(`http://localhost:4000/GetReporte21`)
        const data = await res.json();
        this.setState({ prueba: data })
        console.log(data);
    }

    handleSubmit = async e => {
        e.preventDefault()
        var doc = new jsPDF('p', 'pt');
        doc.setFont('Arial', 'normal')
        doc.text(250,35, "Reporte No. 21")
        doc.text(115,60, `Predicciones de casos y muertes en todo el mundo`)
        doc.setFontSize('15')
        doc.text(100,95,`Se realizó con una regresión polinomial de grado ${this.state.prueba.grado}\nCon un error cuadratico (RMSE) medio de : ${this.state.prueba.RMSE1}\ny un porcentaje de variación (R2) de: ${this.state.prueba.R21}\ncon una prediccion de ${this.state.prueba.pred1}, muertes`) 
        doc.addImage(`data:image/png;base64,${this.state.prueba.imagen1}`,'PNG',50,175,500,500)
        doc.setFontSize('16')
        doc.text(35,805,"Organizacion de Lenguajes y Compiladores 2")
        doc.text(35,825,"Fernando Alberto Ambrosio Alemán                                                    201404106")
        doc.addPage()
        doc.text(115,60, `Predicciones de casos y muertes en todo el mundo`)
        doc.setFontSize('15')
        doc.text(100,95,`Se realizó con una regresión polinomial de grado ${this.state.prueba.grado}\nCon un error cuadratico (RMSE) medio de : ${this.state.prueba.RMSE2}\ny un porcentaje de variación (R2) de: ${this.state.prueba.R22}\ncon una prediccion de ${this.state.prueba.pred2}, muertes`) 
        doc.addImage(`data:image/png;base64,${this.state.prueba.imagen2}`,'PNG',50,175,500,500)
        doc.setFontSize('15')
        doc.text(35,690,`Conclusión: ${this.state.prueba.Conclusion}`)
        doc.setFontSize('16')
        doc.text(35,805,"Organizacion de Lenguajes y Compiladores 2")
        doc.text(35,825,"Fernando Alberto Ambrosio Alemán                                                    201404106")
        doc.save("Reporte21.pdf")
    }
    
    render() {
        return (

            <div>
                <NavegacionInit />
                <div className="main-container col-12">
                    <h1>Reporte No.21</h1>
                    <h3>Predicciones de casos y muertes en todo el mundo</h3>
                    <Button variant="primary" onClick={this.handleSubmit}>
                            Download
                    </Button>
                    <Table>
                        <tbody align="center">
                            <tr>
                                <td>
                                    A continuación se presenta el Predicciones de casos y muertes en todo el mundo<br></br>
                                    Se realizó con una regresión polinomial de grado {this.state.prueba.grado}<br></br>
                                    Con un error cuadratico (RMSE) medio de : {this.state.prueba.RMSE1}<br></br>
                                    y un porcentaje de variación (R2) de: {this.state.prueba.R21}<br></br>
                                    con una prediccion de {this.state.prueba.pred1}, muertes

                                </td>
                            </tr>
                            <tr>
                                <td>
                                    {this.state.prueba.imagen1 ?
                                        <img width='750' height='750' src={`data:image/png;base64,${this.state.prueba.imagen1}`} /> :
                                    ''}
                                </td>

                            </tr>

                            <tr>
                                <td>
                                A continuación se presenta el Predicciones de casos y muertes en todo el mundo<br></br>
                                    Se realizó con una regresión polinomial de grado {this.state.prueba.grado}<br></br>
                                    Con un error cuadratico (RMSE) medio de : {this.state.prueba.RMSE2}<br></br>
                                    y un porcentaje de variación (R2) de: {this.state.prueba.R22}<br></br>
                                    con una prediccion de {this.state.prueba.pred2}, muertes

                                </td>
                            </tr>
                            <tr>
                                <td>
                                    {this.state.prueba.imagen2 ?
                                        <img width='750' height='750' src={`data:image/png;base64,${this.state.prueba.imagen2}`} /> :
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
export default VerReporte21;