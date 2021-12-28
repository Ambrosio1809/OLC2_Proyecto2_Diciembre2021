import React from "react";
import {Switch,Route,Redirect} from 'react-router-dom';
import Reporte1 from "../Formularios/Reporte1";
import CargaMasiva from "./CargaArchivo";
import Home from "./Home";
import Parametrizacion from "./Parametrizacion";


const Main =()=>{
    return(
        <Switch>
            <Route path ="/home" component ={()=><Home/>}/>
            <Route path ="/carga" component ={()=><CargaMasiva/>}/>
            <Route path ="/parametros" component ={()=><Parametrizacion/>}/>

            <Route path ="/ParamReporte/1" component={()=><Reporte1/>}/>

            <Redirect to="/home"/>
        </Switch>
    );
}

export default Main;