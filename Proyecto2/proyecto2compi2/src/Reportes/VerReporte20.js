import React from 'react'
import { Table } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavegacionInit from '../components/Navbar';
import {Button } from 'react-bootstrap';
import {jsPDF} from 'jspdf'

class VerReporte20 extends React.Component {

    state = {
        prueba: [],
        a: 0
    }

    async componentDidMount() {
        const res = await fetch(`http://3.16.160.225:4000/GetReporte20`)
        const data = await res.json();
        this.setState({ prueba: data })
        console.log(data);
    }

    handleSubmit = async e => {
        e.preventDefault()
        var doc = new jsPDF('p', 'pt');
        doc.setFont('Arial', 'normal')
        doc.text(250,35, "Reporte No. 20")
        doc.text(45,60, `Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios\ny tasa de muerte por COVID-19`)
        doc.setFontSize('15')
        doc.text(100,95,`Para el primer caso de Casos vs nuevos casos\nse obtuvo la siguiente grafica con una media de: ${this.state.prueba.t1}`) 
        doc.addImage(`data:image/png;base64,${this.state.prueba.imagen1}`,'PNG',50,175,500,500)
        doc.setFontSize('16')
        doc.text(35,805,"Organizacion de Lenguajes y Compiladores 2")
        doc.text(35,825,"Fernando Alberto Ambrosio Alemán                                                    201404106")
        doc.addPage()
        doc.text(45,60, `Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios\n y tasa de muerte por COVID-19`)
        doc.setFontSize('15')
        doc.text(100,95,`Para el segundo caso de Casos vs muertes\nse obtuvo la siguiente grafica con una media de: ${this.state.prueba.t2}`) 
        doc.addImage(`data:image/png;base64,${this.state.prueba.imagen2}`,'PNG',50,175,500,500)
        doc.setFontSize('15')
        doc.text(35,690,`Conclusión: ${this.state.prueba.Conclusion}`)
        doc.setFontSize('16')
        doc.text(35,805,"Organizacion de Lenguajes y Compiladores 2")
        doc.text(35,825,"Fernando Alberto Ambrosio Alemán                                                    201404106")
        doc.save("Reporte20.pdf")
    }
    
    render() {
        return (

            <div>
                <NavegacionInit />
                <div className="main-container col-12">
                    <h1>Reporte No.20</h1>
                    <h3>Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa de muerte por COVID-19</h3>
                    <Button variant="primary" onClick={this.handleSubmit}>
                            Download
                    </Button>
                    <Table>
                        <tbody align="center">
                            <tr>
                                <td>
                                    A continuación se presenta la Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa de muerte por COVID-19:<br></br> 
                                    Para el primer caso de Casos vs nuevos casos<br></br>
                                    se obtuvo la siguiente grafica con una media de: {this.state.prueba.t1}<br></br>
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
                                A continuación se presenta la Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa de muerte por COVID-19:<br></br> 
                                    Para el segundo caso de Casos vs muertes<br></br>
                                    se obtuvo la siguiente grafica con una media de: {this.state.prueba.t2}<br></br>

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
export default VerReporte20;