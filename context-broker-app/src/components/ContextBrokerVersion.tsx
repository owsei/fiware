
import { useEffect, useState } from "react";
import ContextBrokerServices from '../services/ContextBrokerServices';


function ContextBrokerVersion(){

    const [version, setVersion] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');


    useEffect(() => {
        const version=async()=>{ 
            try{
                const data = await ContextBrokerServices.getContextBrokerVersion();
                setVersion(data.orion.version);
            }
            catch(error){
                setError("Error:" + error);
            }
            finally {
                setLoading(false);
            }
            
        }

        version();
    },[]);
    return (
        <>
            Version:{version}
        </>
    )

}

export default ContextBrokerVersion;