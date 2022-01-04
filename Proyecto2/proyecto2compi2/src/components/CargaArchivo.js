import React, {useState} from 'react';
import NavegacionInit from './Navbar';

function CargaMasiva (){

    const [archivos, setArchivos]=useState(null);

    const subirArchivos=e=>{
        setArchivos(e);
    }

    const insertarArchivos=async()=>{
        const f = new FormData();

        for (let index = 0; index < archivos.length; index ++){
            f.append("files", archivos[index]);            
        }
        try{
            console.log(f)
            let config ={
                method: 'POST',
                headers:{ },
                body: f
                
            }
            await fetch('http://3.16.160.225:4000/CargarArchivo',config)
            .then(response=>response.json())
            .then(data => console.log(data.message))
            .catch(error=>{
                console.log(error)
            })

        }catch(error){

        }
    }

    
        return(
            <div>
                <NavegacionInit/>
                <div className="main-container col-12">
                    <h1>
                        CargaMasiva
                    </h1>
                    <input type="file" name ="files" accept=".csv,.xls,.xlsx,.json" onChange={(e)=>subirArchivos(e.target.files)}/>
                    <button className="btn btn-primary" onClick={()=>insertarArchivos()}>Cargar Archivo</button>


                </div>
            </div>
        )
    
}

export default CargaMasiva;