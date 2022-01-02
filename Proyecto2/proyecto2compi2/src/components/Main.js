import React from "react";
import {Switch,Route,Redirect} from 'react-router-dom';
import Reporte1 from "../Formularios/Reporte1";
import Reporte10 from "../Formularios/Reporte10";
import Reporte11 from "../Formularios/Reporte11";
import Reporte13 from "../Formularios/Reporte13";
import Reporte14 from "../Formularios/Reporte14";
import Reporte15 from "../Formularios/Reporte15";
import Reporte16 from "../Formularios/Reporte16";
import Reporte17 from "../Formularios/Reporte17";
import Reporte19 from "../Formularios/Reporte19";
import Reporte2 from "../Formularios/Reporte2";
import Reporte21 from "../Formularios/Reporte21";
import Reporte22 from "../Formularios/Reporte22";
import Reporte23 from "../Formularios/Reporte23";
import Reporte24 from "../Formularios/Reporte24";
import Reporte25 from "../Formularios/Reporte25";
import Reporte4 from "../Formularios/Reporte4";
import Reporte5 from "../Formularios/Reporte5";
import Reporte6 from "../Formularios/Reporte6";
import Reporte7 from "../Formularios/Reporte7";
import Reporte8 from "../Formularios/Reporte8";
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
            <Route path ="/ParamReporte/6" component={()=><Reporte6/>}/>
            <Route path ="/ParamReporte/7" component={()=><Reporte7/>}/>
            <Route path ="/ParamReporte/8" component={()=><Reporte8/>}/>
            <Route path ="/ParamReporte/9" component={()=><Reporte9/>}/>
            <Route path ="/ParamReporte/10" component={()=><Reporte10/>}/>
            <Route path ="/ParamReporte/11" component={()=><Reporte11/>}/>
            <Route path ="/ParamReporte/13" component={()=><Reporte13/>}/>
            <Route path ="/ParamReporte/14" component={()=><Reporte14/>}/>
            <Route path ="/ParamReporte/15" component={()=><Reporte15/>}/>
            <Route path ="/ParamReporte/16" component={()=><Reporte16/>}/>
            <Route path ="/ParamReporte/17" component={()=><Reporte17/>}/>
            <Route path ="/ParamReporte/19" component={()=><Reporte19/>}/>
            <Route path ="/ParamReporte/21" component={()=><Reporte21/>}/>
            <Route path ="/ParamReporte/22" component={()=><Reporte22/>}/>
            <Route path ="/ParamReporte/23" component={()=><Reporte23/>}/>
            <Route path ="/ParamReporte/24" component={()=><Reporte24/>}/>
            <Route path ="/ParamReporte/25" component={()=><Reporte25/>}/>

            <Redirect to="/home"/>
        </Switch>
    );
}

export default Main;