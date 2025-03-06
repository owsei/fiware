

import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import ContextBrokerVersion from './ContextBrokerVersion';

function Menu() {





    return (
      <>
        <Tabs defaultActiveKey="home" id="uncontrolled-tab-example" className="mb-3" fill>
          <Tab eventKey="home" title="Home">
            Context Broker is alive: <br/>
            &nbsp;<ContextBrokerVersion/>
          </Tab>
          <Tab eventKey="profile" title="Clientes">
            Tab content for Profile
          </Tab>
          <Tab eventKey="contact" title="Verticales">
            Tab content for Verticales
          </Tab>
        </Tabs>
        
      </>
    )
  }
  
  export default Menu