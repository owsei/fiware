
import axios from "axios";

const cbURI='http://localhost:1026/version';

const ContextBrokerServices= {
    
    getContextBrokerVersion : async ()=>{
        try {
            const response = await axios.get(`${cbURI}`);
            return await response.data;
          } catch (error) {
            if (axios.isAxiosError(error)) {
                throw new Error(error.response?.data?.message || "Error en la solicitud");
            } else {
                throw new Error("Error en la solicitud");
            }
          }
    }
   

}


export default ContextBrokerServices;