import React from 'react'
import { Table } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavegacionInit from '../components/Navbar';
import {Button } from 'react-bootstrap';
import {jsPDF} from 'jspdf'

class VerReporte11 extends React.Component {

    state = {
        prueba: [],
        a: 0
    }

    async componentDidMount() {
        const res = await fetch(`http://3.16.160.225:4000/GetReporte11`)
        const data = await res.json();
        this.setState({ prueba: data })
        console.log(data);
    }

    handleSubmit = async e => {
        e.preventDefault()
        var doc = new jsPDF('p', 'pt');
        doc.setFont('Arial', 'normal')
        doc.text(250,35, "Reporte No. 11")
        doc.text(45,60, `Porcentaje de hombres infectados por covid-19 en ${this.state.prueba.pais} desde\nel primer caso activo`)
        doc.setFontSize('15')
        doc.text(45,95,`A continuación se presenta el Porcentaje de hombres infectados por covid-19 en\n${this.state.prueba.pais} desde el primer caso activo En el cual podemos observar que los hombres\npresentan un porcentaje de ${this.state.prueba.porcentaje}% lo cual nos puede dar una breve descripción de como se\ncomporta el genero masculino frente a la infección por covid 19`) 
        doc.addImage(`data:image/png;base64,${this.state.prueba.imagen}`,'PNG',50,200,500,500)
        doc.setFontSize('15')
        doc.text(35,715,`Conclusión: ${this.state.prueba.Conclusion}`)
        doc.setFontSize('16')
        doc.text(35,805,"Organizacion de Lenguajes y Compiladores 2")
        doc.text(35,825,"Fernando Alberto Ambrosio Alemán                                                    201404106")
        doc.save("Reporte11.pdf")
    }
    
    render() {
        return (

            <div>
                <NavegacionInit />
                <div className="main-container col-12">
                    <h1>Reporte No.11</h1>
                    <h3>Porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo</h3>
                    <Button variant="primary" onClick={this.handleSubmit}>
                            Download
                    </Button>
                    <Table>
                        <tbody align="center">
                            <tr>
                                <td>
                                    A continuación se presenta el Porcentaje de hombres infectados por covid-19 en {this.state.prueba.pais} desde el primer caso activo<br></br>
                                    En el cual podemos observar que los hombres presentan un porcentaje de {this.state.prueba.porcentaje} lo cual nos puede dar una breve <br></br>
                                    descripción de como se comporta el genero masculino frente a la infección por covid 19

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
export default VerReporte11;