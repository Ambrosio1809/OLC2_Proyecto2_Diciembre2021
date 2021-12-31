import React from 'react'
import NavegacionInit from './Navbar';
import {Table} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

class SeleccionReporte extends React.Component{
    state ={
        prueba :[]
    }

    Ver= async (identificador) =>{
        window.location.href="/VerReporte/"+identificador
    }

    render(){
        return(
            <div>
                <NavegacionInit/>
                <div className="main-container col-12" align='center'>
                    <h1>Seleccione el reporte que desea ver</h1>
                <Table>
                    <thead>
                        <tr>
                            <th>No.</th><th>Descripción</th>
                            <th>Ver</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1.</td><td>Tendencia de la infección por Covid-19 en un País</td>
                            <td><button onClick={()=>this.Ver(1)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>2.</td><td>Prediccion de infertados en un País</td>
                            <td><button onClick={()=>this.Ver(2)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr> 
                        <tr>
                            <td>3.</td><td>Indice de progresión de la pandemia</td>
                            <td><button onClick={()=>this.Ver(3)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr> 
                        <tr>
                            <td>4.</td><td>Prediccion de mortalidad por COVID en un departamento</td>
                            <td><button onClick={()=>this.Ver(4)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr> 
                        <tr>
                            <td>5.</td><td>Prediccion de mortalidad por COVID en un País</td>
                            <td><button onClick={()=>this.Ver(5)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr> 
                        <tr>
                            <td>6.</td><td>Análisis del número de muertes por Coronavirus en un país</td>
                            <td><button onClick={()=>this.Ver(6)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr> 
                        <tr>
                            <td>7.</td><td>Tendencia del número de infectados por día de un País</td>
                            <td><button onClick={()=>this.Ver(7)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr> 
                        <tr>
                            <td>8.</td><td>Prediccion de casos de un país para un año</td>
                            <td><button onClick={()=>this.Ver(8)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr> 
                        <tr>
                            <td>9.</td><td>Tendencia de la vacunación de un país</td>
                            <td><button onClick={()=>this.Ver(9)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr> 
                        <tr>
                            <td>10.</td><td>Analisis comparativo de vacunación entre 2 paises</td>
                            <td><button onClick={()=>this.Ver(10)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr> 
                        <tr>
                            <td>11.</td><td>Porcentaje de hombres infectados por covid-19 en un país desde el primer caso activo</td>
                            <td><button onClick={()=>this.Ver(11)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr> 
                        <tr>
                            <td>12.</td><td>Analisis comparativo entre 2 o más paises o continentes</td>
                            <td><button onClick={()=>this.Ver(12)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>13.</td><td>Muertes promedio por casos confirmados y edad de covid 19 en un pais</td>
                            <td><button onClick={()=>this.Ver(13)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>14.</td><td>Muertes según regiones de un país Covid-19</td>
                            <td><button onClick={()=>this.Ver(14)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>15.</td><td>Tendencia de casos confirmados de Coronavirus en un departamento de un país</td>
                            <td><button onClick={()=>this.Ver(15)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>16.</td><td>Porcentaje de muertes frente al total de casos en un país, región o continente</td>
                            <td><button onClick={()=>this.Ver(16)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>17.</td><td>Tasa de comportamiento de casos activos en relación al número de muertes en un continente</td>
                            <td><button onClick={()=>this.Ver(17)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>18.</td><td>Comportamiento y clasificacion de personas infectadas por covid-19 por municipio en un país</td>
                            <td><button onClick={()=>this.Ver(18)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>19.</td><td>Predicción de muertes en el ultimo día del primer año de infecciones en un país</td>
                            <td><button onClick={()=>this.Ver(19)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>20.</td><td>Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa de muerte por COVID-19</td>
                            <td><button onClick={()=>this.Ver(20)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>21.</td><td>Predicciones de casos y muertes en todo el mundo - Neural Network MLPRegressor</td>
                            <td><button onClick={()=>this.Ver(21)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>22.</td><td>Tasa de mortalidad por coronavirus (COVID-19) en un país</td>
                            <td><button onClick={()=>this.Ver(22)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>23.</td><td>Factores de muerte por COVID-19 en un país</td>
                            <td><button onClick={()=>this.Ver(23)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>24.</td><td>Comparación entre el número de casos detectados y el número de pruebas de un país</td>
                            <td><button onClick={()=>this.Ver(24)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                        <tr>
                            <td>25.</td><td>Predicción de casos confirmados por día</td>
                            <td><button onClick={()=>this.Ver(25)} type="button" className="btn btn-primary">Ver</button></td>
                        </tr>
                    </tbody>                                            
                </Table>                
            </div>
            </div>
        )
    }
}
export default SeleccionReporte;