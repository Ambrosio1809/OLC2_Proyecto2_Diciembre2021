import React from "react";
import { Form, Button } from 'react-bootstrap';
import NavegacionInit from "../components/Navbar";
import '../components/Design.css'

class Reporte16 extends React.Component {
    state = {
        form: {
            Variable1: '',
            Variable2: '',
            Variable3: '',
            Variable4: '',
            Variable5: '',
            Variable6: '',
            Variable7: '',
            Variable8: '',
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
            let res = await fetch('http://localhost:4000/Reporte16', config)
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
                    <h1>Parametros Reporte No.16</h1>
                    <Form onSubmit={this.handleSubmit}>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese el País</Form.Label>
                            <Form.Control type="text" name="Variable1" placeholder="Nombre_País" onChange={this.handleChange} value={this.state.form.Variable1} />
                        </Form.Group>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese Nombre Columna Para Pais</Form.Label>
                            <Form.Control type="text" name="Variable2" placeholder="Columna_pais" onChange={this.handleChange} value={this.state.form.Variable2} />
                        </Form.Group>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese la Region</Form.Label>
                            <Form.Control type="text" name="Variable3" placeholder="Nombre_Region" onChange={this.handleChange} value={this.state.form.Variable3} />
                        </Form.Group>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese Nombre Columna Para Región</Form.Label>
                            <Form.Control type="text" name="Variable4" placeholder="Columna_Region" onChange={this.handleChange} value={this.state.form.Variable4} />
                        </Form.Group>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese Continente</Form.Label>
                            <Form.Control type="text" name="Variable5" placeholder="Nombre_Continente" onChange={this.handleChange} value={this.state.form.Variable5} />
                        </Form.Group>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese Nombre Columna Para Continente</Form.Label>
                            <Form.Control type="text" name="Variable6" placeholder="Columna_Continente" onChange={this.handleChange} value={this.state.form.Variable6} />
                        </Form.Group>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese Nombre Columna Para Muertes</Form.Label>
                            <Form.Control type="text" name="Variable7" placeholder="Columna_Muertes" onChange={this.handleChange} value={this.state.form.Variable7} />
                        </Form.Group>
                        <Form.Group controlId="formUsename">
                            <Form.Label>Ingrese Nombre Columna Para Casos</Form.Label>
                            <Form.Control type="text" name="Variable8" placeholder="Columna_Casos" onChange={this.handleChange} value={this.state.form.Variable8} />
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

export default Reporte16;