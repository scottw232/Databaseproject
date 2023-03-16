import React, { useState, useEffect } from 'react'
import { Card, Form, Button, Container, Row, Col, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import axios from "axios";
import $ from 'jquery';

export default function Postal({ addNewData, currData }) {

  const [formState, setForm] = useState(false)
  const [postalData, setPostalData] = useState({'postal_code': null, 'city': null, 'state': null})


  useEffect(() => {

  }, [])

  const handlePostal = async (e) => {
    let data = await validatePostal($('#postalCode').val() === '' ? 0 : $('#postalCode').val())
    console.log(data)
    setPostalData(data)
    setForm(true)
  }

  const validatePostal = async (postalInput) => {
    try {
      let res = await axios.post("validate_postal_code" + "?postal_code=" + postalInput)
      let result = res.data
      return result
    } catch(err) {
      console.log(err)
    }
  };

  const handlePostalConfirm = () => {
    console.log("Postal Data: " + postalData.postal_code)
    addNewData("postal", postalData)
  }

  const handlePostalCancel = () => {
    setForm(false)
  }

  let postalForm = (
      <Form onSubmit={handlePostal}>
        <Form.Group className="mb-3 text-start" controlId="postalCode">
          <Form.Label>Please enter your five digit postal code:</Form.Label>
          <Form.Control type="text" placeholder="Enter postal code" />
        </Form.Group>
        <Button variant="primary" onClick={handlePostal}>
          Submit
        </Button>
      </Form>
    )

  if (formState) {
    let temp = (<></>)
    if (!postalData.hasOwnProperty('valid')) {
      temp = (
        <>
          <Row >
            <Col className='mb-4'>
              You entered the following postal code:
            </Col>
          </Row>
          <Row >
            <Col className='fw-bold'>
              {postalData.postal_code}
            </Col>
          </Row>
          <Row >
            <Col className='mb-4 fw-bold'>
              {postalData.city}, {postalData.state}
            </Col>
          </Row>
          <Row>
            <Col>
             Is this correct?
            </Col>
          </Row>
          <Row>
            <Col>
              <Link to='/household'>
                <Button variant="primary" type="submit" size='lg'
                  onClick={handlePostalConfirm}>
                  Yes
                </Button>
              </Link>
            </Col>
            <Col>
              <Button variant="primary" type="submit" size='lg'
                onClick={handlePostalCancel}>
                No
              </Button>
            </Col>
          </Row>
        </>
      )
    }
    else {
      temp = (
        <>
          <Row className='mb-4'>
            <Col>
              Invalid postal code. Please go back and try again.
            </Col>
          </Row>
          <Row >
            <Button variant="primary" type="submit" size='lg'
                onClick={e => setForm(false)}>
                Back
            </Button>
          </Row>
        </>
      )
    }

    postalForm = (
      <>
        <Container>
          {temp}
        </Container>
      </>
    )
  }

  return (
    <>
      <Card border="dark" style={{margin: '1rem 3em'}}>
        <Card.Header style={{background: 'DarkGray' }}><h3 className='m-0'>Enter household info</h3></Card.Header>
        <Card.Body className='p-3'>
          {postalForm}
        </Card.Body>
      </Card>
    </>
  )
}
