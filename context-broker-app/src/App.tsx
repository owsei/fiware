import './App.css'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Menu from './components/Menu';

import CBVersions from './components/CBVersions';


function App() {
  
  return (
    <>
     <Container fluid>
      <Row>
        <Col><h2>Context Broker CB</h2></Col>
      </Row>
      <Row>
        <Col>
          <Menu/>
        </Col>
      </Row>
    </Container>
    </>
  )
}

export default App
