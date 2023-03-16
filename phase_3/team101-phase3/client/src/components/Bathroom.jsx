import React, { useState } from 'react'
import { Table, Card, Col, Container, Form, Row, Button, ButtonGroup, ToggleButton,} from 'react-bootstrap';
import { Link } from "react-router-dom";
import $ from 'jquery';

export default function Bathroom({ insertBathrmCallback, addNewData, currData }) {

  const [radioValue, setRadioValue] = useState('full')
  const [addBathroom, setCurrentForm] = useState(true)
  const [bathroomList, setBathroomList] = useState([])
  const [isPrimary, setPrimary] = useState(false)
  const [hasPrimary, setHasPrimary] = useState(false)
  const [bathroomID, setBathroomID] = useState(1)



  const handleAddBathroom = (e) => {
    let temp = bathroomList
    let info = {}
    info['bathroom_number'] = bathroomID
    info['type'] = radioValue
    info['number_of_sinks'] = $('#sinks').val() === '' ? 0 : $('#sinks').val()
    info['number_of_commodes'] = $('#commodes').val() === '' ? 0 : $('#commodes').val()
    info['number_of_bidets'] = $('#bidets').val() === '' ? 0 : $('#bidets').val()
    if (radioValue === 'full') {
      info['number_of_bathtubs'] = $('#bathtubs').val() === '' ? 0 : $('#bathtubs').val()
      info['number_of_showers'] = $('#showers').val() === '' ? 0 : $('#showers').val()
      info['number_of_tub_showers'] = $('#tubShowers').val() === '' ? 0 : $('#tubShowers').val()
      info['is_primary_bathroom'] = true
      setHasPrimary(true)
      if (!isPrimary || hasPrimary) {
        info['is_primary_bathroom'] = false
      }
    }
    temp.push(info)
    setBathroomID(bathroomID+1)
    setBathroomList(temp)
    setCurrentForm(e)
  }

  const handleAddList = () => {
    addNewData("bathrooms", bathroomList)
    insertBathrmCallback()
  }

  const radios = [
    { name: 'Full', value: 'full' },
    { name: 'Half', value: 'half' },
  ]

  let currForm = (
    <>
      <div className='mb-4'>Please provide the details regard the bathroom.</div>
      <Container className='mb-4' fluid>
        <Row className='mb-4'>
          <Col>Bathroom type:</Col>
          <Col>
            <ButtonGroup>
              {radios.map((radio, idx) => (
                <ToggleButton
                  key={idx}
                  id={`radio-${idx}`}
                  type="radio"
                  variant="outline-primary"
                  name="radio"
                  value={radio.value}
                  checked={radioValue === radio.value}
                  onChange={(e) => setRadioValue(e.currentTarget.value)}
                >
                  {radio.name}
                </ToggleButton>
              ))}
            </ButtonGroup>
          </Col>
        </Row>
        <Row>

          <Col>
            <Form.Group className="mb-3" controlId="sinks">
              <Container fluid>
                <Row>
                  <Col className="text-start">
                    <Form.Label className='mt-2'>Sinks:</Form.Label>
                  </Col>
                  <Col>
                  <Form.Control type="number" placeholder="2" />
                  </Col>
                </Row>
              </Container>
            </Form.Group>
          </Col>

          <Col >
            <Form.Group className="mb-3" controlId="bathtubs">
                <Container fluid>
                  <Row>
                    <Col className="text-start">
                      <Form.Label className='mt-2'>Bathtubs:</Form.Label>
                    </Col>
                    <Col>
                    <Form.Control type="number" placeholder="0" disabled={radioValue === 'half'}/>
                    </Col>
                  </Row>
                </Container>
              </Form.Group>
          </Col>

        </Row>
        <Row>

          <Col>
            <Form.Group className="mb-3" controlId="commodes">
              <Container fluid>
                <Row>
                  <Col className="text-start">
                    <Form.Label className='mt-2'>Commodes:</Form.Label>
                  </Col>
                  <Col>
                  <Form.Control type="number" placeholder="2" />
                  </Col>
                </Row>
              </Container>
            </Form.Group>
          </Col>

          <Col >
            <Form.Group className="mb-3" controlId="showers">
                <Container fluid>
                  <Row>
                    <Col className="text-start">
                      <Form.Label className='mt-2'>Showers:</Form.Label>
                    </Col>
                    <Col>
                    <Form.Control type="number" placeholder="0" disabled={radioValue === 'half'}/>
                    </Col>
                  </Row>
                </Container>
              </Form.Group>
          </Col>

        </Row>
        <Row>

          <Col>
            <Form.Group className="mb-3" controlId="bidets">
              <Container fluid>
                <Row>
                  <Col className="text-start">
                    <Form.Label className='mt-2'>Bidets:</Form.Label>
                  </Col>
                  <Col>
                  <Form.Control type="number" placeholder="2" />
                  </Col>
                </Row>
              </Container>
            </Form.Group>
          </Col>

          <Col >
            <Form.Group className="mb-3" controlId="tubShowers">
                <Container fluid>
                  <Row>
                    <Col className="text-start">
                      <Form.Label className='mt-2'>Tub/showers:</Form.Label>
                    </Col>
                    <Col>
                    <Form.Control type="number" placeholder="0" disabled={radioValue === 'half'}/>
                    </Col>
                  </Row>
                </Container>
              </Form.Group>
          </Col>

        </Row>

        <Row>
          <Form style={{marginLeft: '12px', display: 'flex', justifyContent: 'center'}}>
            <Form.Check
              disabled={radioValue === 'half' || hasPrimary === true}
              type="switch"
              checked={isPrimary}
              id="primaryBath"
              label="This is a primary bathroom"
              className='text-start'
              onChange={e => setPrimary(e.target.checked)}
            />
          </Form>
          </Row>
      </Container>

      <Button size='lg' onClick={() => handleAddBathroom(false)}>
        Add
      </Button>
    </>
  )

  if (!addBathroom) {
    currForm = (
      <>
        <div className='mb-4'>
          You have added the following bathrooms to your household:
        </div>
        <Table className='mb-0' striped bordered hover>
          <thead>
            <tr>
              <th>Bathroom #</th>
              <th>Type</th>
              <th>Primary</th>
            </tr>
          </thead>
          <tbody>
            {
              bathroomList.map(function (e, idx) {
                return (
                  <tr key={idx}>
                    <td>{e.bathroom_number}</td>
                    <td>{e.type}</td>
                    <td>{e.is_primary_bathroom ? 'Yes' : ''}</td>
                  </tr>
                )
              })
            }
          </tbody>
        </Table>
        <div className='mb-4 text-end'>
          <Link onClick={() => setCurrentForm(true)}>+ Add another bathroom</Link>
        </div>
        <Link to='/appliance'>
          <Button size='lg' onClick={handleAddList}>
            Next
          </Button>
        </Link>
      </>
    )
  }

  return (
    <>
      <Card border="dark" style={{margin: '1rem 3em'}}>
        <Card.Header style={{background: 'DarkGray' }}>
          <h3 className='m-0'>{addBathroom ? 'Add bathroom' : 'Bathrooms'}</h3>
        </Card.Header>
        <Card.Body className='p-3'>
          {currForm}
        </Card.Body>
      </Card>
    </>
  )
}
