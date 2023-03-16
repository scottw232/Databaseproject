import { React, useState } from 'react'
import { Card, Col, Container, Form, Row, Button, ButtonGroup, ToggleButton,} from 'react-bootstrap';
import axios from "axios";
import { Link } from "react-router-dom";
import $ from 'jquery';

export default function Household({ insertHouseCallback, addNewData, currData }) {

  const [isAfterPhone, setCurrentForm] = useState(false)
  const [radioValue, setRadioValue] = useState('1')

  const radios = [
    { name: 'Yes', value: '1' },
    { name: 'No', value: '2' },
  ]

  const handleAddPhone = async (e) => {
    let phoneData = {}
    let data
    if (radioValue === '1') {
      phoneData['phone_number'] = parseInt($('#phoneNumber').val())
      phoneData['area_code'] = parseInt($('#areaCode').val())
      phoneData['phone_type'] = $('#phoneType').val()
      data = await validatePhone(phoneData.phone_number, phoneData.area_code)
    }
    if ((radioValue === '2') || (data !== undefined)) {
      addNewData("phone", 'none')
      setCurrentForm(true)
    }

  }

  const validatePhone = async (phone, areaCode) => {
    try {
      let req = "/validate_phone_number?area_code=" + areaCode + "&seven_digits=" + phone
      let res = await axios.post(req)
      return res.data
    } catch (err) {
      window.alert(err.response.data.message)
    }
  }

  const handleAddHome = (e) => {
    let homeData = {}
    homeData['square_footage'] = $('#sqFootage').val() === '' ? 1 : $('#sqFootage').val()
    homeData['number_of_occupants'] = $('#occupants').val() === '' ? 1 : $('#occupants').val()
    homeData['number_of_bedrooms'] = $('#bedrooms').val() === '' ? 1 : $('#bedrooms').val()
    homeData['household_type'] = $('#homeType').val()
    console.log(homeData['square_footage'])
    addNewData("household", homeData)
    insertHouseCallback()
  }

  let currForm = (
    <>
      <Container fluid>
        <Row>
          <Col className="text-start">
            Would you like to enter a phone number?
          </Col>
          <Col className="align-self-end">
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
      </Container>
      <div className="text-start mb-2" style={{marginLeft: '12px'}}>Please enter your phone number.</div>
      <Form>
        <Form.Group className="mb-3" controlId="areaCode">
          <Container fluid>
            <Row>
              <Col className="text-start">
                <Form.Label className='mt-2'>Area Code:</Form.Label>
              </Col>
              <Col xs={10}>
                <Form.Control type="text" placeholder="404" disabled={radioValue === '2'} />
              </Col>
            </Row>
          </Container>
        </Form.Group>

        <Form.Group className="mb-3" controlId="phoneNumber">
          <Container fluid>
            <Row>
              <Col className="text-start">
                <Form.Label className='mt-2'>Number:</Form.Label>
              </Col>
              <Col xs={10}>
              <Form.Control type="text" disabled={radioValue === '2'}/>
              </Col>
            </Row>
          </Container>
        </Form.Group>

        <Form.Group className="mb-3" controlId="phoneType">
          <Container fluid>
            <Row>
              <Col className="text-start">
                <Form.Label className='mt-2'>Phone Type:</Form.Label>
              </Col>
              <Col xs={10}>
                <Form.Select aria-label="Default select example" disabled={radioValue === '2'}>
                  <option value="home">Home</option>
                  <option value="mobile">Mobile</option>
                  <option value="work">Work</option>
                  <option value="other">Other</option>
                </Form.Select>
              </Col>
            </Row>
          </Container>

        </Form.Group>
      </Form>
      <Button size='lg' onClick={handleAddPhone}>
        Next
      </Button>
    </>
  )

  if (isAfterPhone) {
    currForm = (
      <>
        <div className="text-start mb-2" style={{marginLeft: '12px'}}>
          Please enter the following details for your household.
        </div>
        <Form>
          <Form.Group className="mb-3" controlId="homeType">
            <Container fluid>
              <Row>
                <Col className="text-start">
                  <Form.Label className='mt-2'>Home type:</Form.Label>
                </Col>
                <Col xs={10}>
                  <Form.Select aria-label="Default select example">
                    <option value="house">House</option>
                    <option value="apartment">Apartment</option>
                    <option value="townhome">Townhome</option>
                    <option value="condominium">Condominium</option>
                    <option value="mobile home">Mobile home</option>
                  </Form.Select>

                </Col>
              </Row>
            </Container>
          </Form.Group>

          <Form.Group className="mb-3" controlId="sqFootage">
            <Container fluid>
              <Row>
                <Col className="text-start">
                  <Form.Label className='mt-2'>Square footage:</Form.Label>
                </Col>
                <Col xs={10}>
                <Form.Control type="text"/>
                </Col>
              </Row>
            </Container>
          </Form.Group>

          <Form.Group className="mb-3" controlId="occupants">
            <Container fluid>
              <Row>
                <Col className="text-start">
                  <Form.Label className='mt-2'>Occupants:</Form.Label>
                </Col>
                <Col xs={10}>
                <Form.Control type="number" placeholder="4" />
                </Col>
              </Row>
            </Container>
          </Form.Group>

          <Form.Group className="mb-3" controlId="bedrooms">
            <Container fluid>
              <Row>
                <Col className="text-start">
                  <Form.Label className='mt-2'>Bedrooms:</Form.Label>
                </Col>
                <Col xs={10}>
                <Form.Control type="number" placeholder="3" />
                </Col>
              </Row>
            </Container>
          </Form.Group>
        </Form>
        <Link to='/bathroom'>
          <Button size='lg' onClick={handleAddHome}>
              Next
          </Button>
        </Link>


      </>
    )
  }

  return (
    <>
    <Card border="dark" style={{margin: '1rem 3em'}}>
      <Card.Header style={{background: 'DarkGray' }}><h3 className='m-0'>Enter household info</h3></Card.Header>
      <Card.Body className='p-3'>
        {currForm}
      </Card.Body>
    </Card>
  </>
  )
}
