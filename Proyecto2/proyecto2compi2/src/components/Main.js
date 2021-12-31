import React from "react";
import {Switch,Route,Redirect} from 'react-router-dom';
import Reporte1 from "../Formularios/Reporte1";
import Reporte2 from "../Formularios/Reporte2";
import Reporte4 from "../Formularios/Reporte4";
import Reporte5 from "../Formularios/Reporte5";
import Reporte9 from "../Formularios/Reporte9";
import VerReporte1 from "../Reportes/VerReporte1";
import CargaMasiva from "./CargaArchivo";
import Home from "./Home";
import Parametrizacion from "./Parametrizacion";
import SeleccionReporte from "./SeleccionReporte";


const Main =()=>{
    return(
        <Switch>
            <Route path ="/home" component ={()=><Home/>}/>
            <Route path ="/carga" component ={()=><CargaMasiva/>}/>
            <Route path ="/parametros" component ={()=><Parametrizacion/>}/>
            <Route path ="/Seleccion" component ={()=><SeleccionReporte/>}/>

            <Route path ="/ParamReporte/1" component={()=><Reporte1/>}/>
            <Route path ="/VerReporte/1" component={()=><VerReporte1/>}/>

            <Route path ="/ParamReporte/2" component={()=><Reporte2/>}/>


            <Route path ="/ParamReporte/4" component={()=><Reporte4/>}/>

            <Route path ="/ParamReporte/5" component={()=><Reporte5/>}/>
            <Route path ="/ParamReporte/9" component={()=><Reporte9/>}/>

            <Redirect to="/home"/>
        </Switch>
    );
}

export default Main;