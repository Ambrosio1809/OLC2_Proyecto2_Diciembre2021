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
import Reporte18 from "../Formularios/Reporte18";
import Reporte19 from "../Formularios/Reporte19";
import Reporte2 from "../Formularios/Reporte2";
import Reporte20 from "../Formularios/Reporte20";
import Reporte21 from "../Formularios/Reporte21";
import Reporte22 from "../Formularios/Reporte22";
import Reporte23 from "../Formularios/Reporte23";
import Reporte24 from "../Formularios/Reporte24";
import Reporte25 from "../Formularios/Reporte25";
import Reporte3 from "../Formularios/Reporte3";
import Reporte4 from "../Formularios/Reporte4";
import Reporte5 from "../Formularios/Reporte5";
import Reporte6 from "../Formularios/Reporte6";
import Reporte7 from "../Formularios/Reporte7";
import Reporte8 from "../Formularios/Reporte8";
import Reporte9 from "../Formularios/Reporte9";
import VerReporte1 from "../Reportes/VerReporte1";
import VerReporte10 from "../Reportes/VerReporte10";
import VerReporte11 from "../Reportes/VerReporte11";
import VerReporte13 from "../Reportes/VerReporte13";
import VerReporte14 from "../Reportes/VerReporte14";
import VerReporte15 from "../Reportes/VerReporte15";
import VerReporte16 from "../Reportes/VerReporte16";
import VerReporte17 from "../Reportes/VerReporte17";
import VerReporte18 from "../Reportes/VerReporte18";
import VerReporte19 from "../Reportes/VerReporte19";
import VerReporte2 from "../Reportes/VerReporte2";
import VerReporte20 from "../Reportes/VerReporte20";
import VerReporte21 from "../Reportes/VerReporte21";
import VerReporte22 from "../Reportes/VerReporte22";
import VerReporte23 from "../Reportes/VerReporte23";
import VerReporte24 from "../Reportes/VerReporte24";
import VerReporte25 from "../Reportes/VerReporte25";
import VerReporte3 from "../Reportes/VerReporte3";
import VerReporte4 from "../Reportes/VerReporte4";
import VerReporte5 from "../Reportes/VerReporte5";
import VerReporte6 from "../Reportes/VerReporte6";
import VerReporte7 from "../Reportes/VerReporte7";
import VerReporte8 from "../Reportes/VerReporte8";
import VerReporte9 from "../Reportes/VerReporte9";
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
            <Route path ="/VerReporte/2" component={()=><VerReporte2/>}/>

            <Route path ="/ParamReporte/3" component={()=><Reporte3/>}/>
            <Route path ="/VerReporte/3" component={()=><VerReporte3/>}/>

            <Route path ="/ParamReporte/4" component={()=><Reporte4/>}/>
            <Route path ="/VerReporte/4" component={()=><VerReporte4/>}/>

            <Route path ="/ParamReporte/5" component={()=><Reporte5/>}/>
            <Route path ="/VerReporte/5" component={()=><VerReporte5/>}/>

            <Route path ="/ParamReporte/6" component={()=><Reporte6/>}/>
            <Route path ="/VerReporte/6" component={()=><VerReporte6/>}/>

            <Route path ="/ParamReporte/7" component={()=><Reporte7/>}/>
            <Route path ="/VerReporte/7" component={()=><VerReporte7/>}/>

            <Route path ="/ParamReporte/8" component={()=><Reporte8/>}/>
            <Route path ="/VerReporte/8" component={()=><VerReporte8/>}/>

            <Route path ="/ParamReporte/9" component={()=><Reporte9/>}/>
            <Route path ="/VerReporte/9" component={()=><VerReporte9/>}/>

            <Route path ="/ParamReporte/10" component={()=><Reporte10/>}/>
            <Route path ="/VerReporte/10" component={()=><VerReporte10/>}/>

            <Route path ="/ParamReporte/11" component={()=><Reporte11/>}/>
            <Route path ="/VerReporte/11" component={()=><VerReporte11/>}/>

            <Route path ="/ParamReporte/13" component={()=><Reporte13/>}/>
            <Route path ="/VerReporte/13" component={()=><VerReporte13/>}/>

            <Route path ="/ParamReporte/14" component={()=><Reporte14/>}/>
            <Route path ="/VerReporte/14" component={()=><VerReporte14/>}/>

            <Route path ="/ParamReporte/15" component={()=><Reporte15/>}/>
            <Route path ="/VerReporte/15" component={()=><VerReporte15/>}/>
            
            <Route path ="/ParamReporte/16" component={()=><Reporte16/>}/>
            <Route path ="/VerReporte/16" component={()=><VerReporte16/>}/>
            <Route path ="/ParamReporte/17" component={()=><Reporte17/>}/>
            <Route path ="/VerReporte/17" component={()=><VerReporte17/>}/>
            <Route path ="/ParamReporte/18" component={()=><Reporte18/>}/>
            <Route path ="/VerReporte/18" component={()=><VerReporte18/>}/>
            <Route path ="/ParamReporte/19" component={()=><Reporte19/>}/>
            <Route path ="/VerReporte/19" component={()=><VerReporte19/>}/>
            <Route path ="/ParamReporte/20" component={()=><Reporte20/>}/>
            <Route path ="/VerReporte/20" component={()=><VerReporte20/>}/>
            <Route path ="/ParamReporte/21" component={()=><Reporte21/>}/>
            <Route path ="/VerReporte/21" component={()=><VerReporte21/>}/>
            <Route path ="/ParamReporte/22" component={()=><Reporte22/>}/>
            <Route path ="/VerReporte/22" component={()=><VerReporte22/>}/>
            <Route path ="/ParamReporte/23" component={()=><Reporte23/>}/>
            <Route path ="/VerReporte/23" component={()=><VerReporte23/>}/>
            <Route path ="/ParamReporte/24" component={()=><Reporte24/>}/>
            <Route path ="/VerReporte/24" component={()=><VerReporte24/>}/>
            <Route path ="/ParamReporte/25" component={()=><Reporte25/>}/>
            <Route path ="/VerReporte/25" component={()=><VerReporte25/>}/>

            <Redirect to="/home"/>
        </Switch>
    );
}

export default Main;