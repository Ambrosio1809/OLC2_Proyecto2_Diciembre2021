import React from "react";
import { Form, Button } from 'react-bootstrap';
import NavegacionInit from "../components/Navbar";
import '../components/Design.css'

class Reporte17 extends React.Component {
    state = {
        form: {
            Variable1: '',
            Variable2: '',
            Variable3: '',
            Variable4: ''
        }
    }

    handleChange = e => {
        this.setState({
            form: {
                ...this.state.form,
                [e.target.name]: e.target.value
            }
        })
    }

    handleSubmit = async e => {
        e.preventDefault()
        //console.log(this.state.form)

        try {
            let config = {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.state.form)

            }
            let res = await fetch('http://3.16.160.225:4000/Reporte17', config)
            let json = await res.json()
            console.log(json)

        } catch (error) {

        }
        //window.location.href = "/ParamReporte/1"
    }

    render() {
        return (
            <div>
                <NavegacionInit />
                <div className="main-container col-12">
                    <h1>Parametros Reporte No.17</h1>
                    <Form onSubmit={this.handleSubmit}>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese el Continente</Form.Label>
                            <Form.Control type="text" name="Variable1" placeholder="Nombre_Continente" onChange={this.handleChange} value={this.state.form.Variable1} />
                        </Form.Group>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese Nombre Columna Para Continente</Form.Label>
                            <Form.Control type="text" name="Variable2" placeholder="Columna_Continente" onChange={this.handleChange} value={this.state.form.Variable2} />
                        </Form.Group>                        
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese Nombre Columna Para Muertes</Form.Label>
                            <Form.Control type="text" name="Variable3" placeholder="Columna_Muertes" onChange={this.handleChange} value={this.state.form.Variable3} />
                        </Form.Group>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese Nombre Columna Para Casos</Form.Label>
                            <Form.Control type="text" name="Variable4" placeholder="Columna_Casos" onChange={this.handleChange} value={this.state.form.Variable4} />
                        </Form.Group>
                        <Button variant="primary" type="submit" onSubmit={this.handleSubmit}>
                            Visualizar
                        </Button>
                    </Form>
                </div>
            </div>
        )
    }
}

export default Reporte17;