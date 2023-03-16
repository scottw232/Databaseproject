import React from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { useState, useEffect } from "react";
import { Card, Form, Button, Container, Col, Row } from "react-bootstrap";
import $ from 'jquery';

axios.defaults.baseURL = "http://localhost:8080";

export default function Email({ addNewData, currData }) {
  const [email, setEmail] = useState("")
  const [validState, setValidState] = useState(false)

  const handleEmailInput = async (e) => {
    if ($('#formBasicEmail').val() === '') {
      window.alert("Field is empty. Please try again.")
    }
    else {
      let result = await validateEmail($('#formBasicEmail').val())
      setValidState(false)
      if (result) {
        if (result.valid) {
          $('#submitBtn').prop('disabled', false)
          setEmail($('#formBasicEmail').val())
          setValidState(true)
        }
        else {
          window.alert("Email already exists. Please re-enter another email.")
          setEmail("")
        }
      }
    }
  };

  const handleEmailSubmit = () => {
    console.log(email)
    addNewData("email", email)
  }

  const validateEmail = async (emailInput) => {
    try {
      let res = await axios.post("/validate_email" + "?email=" + emailInput)
      let result = res.data
      return result
    } catch(err) {
      window.alert(err.response.data.message)
    }
  };

  return (
    <>
      <Card border="dark" style={{margin: '1rem 3em'}}>
        <Card.Header style={{background: 'DarkGray' }}><h3 className='m-0'>Enter household info</h3></Card.Header>
        <Card.Body className='p-3 text-left'>
        <Form>
            <Form.Group className="mb-3 text-start" controlId="formBasicEmail">
              <Form.Label>Please enter your email address:</Form.Label>
              <Form.Control onChange={e => $('#submitBtn').prop('disabled', true)} type="email" placeholder="Enter email" />
              <Form.Text className="text-muted" >
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>
            <Container>
              <Row>
                <Col>
                  <Button variant="primary" onClick={handleEmailInput}>
                    Check for Validation
                  </Button>
                </Col>
                <Col>
                  {validState ? (
                    <Link  to='/postal'>
                      <Button id='submitBtn' variant="primary" onClick={handleEmailSubmit}>
                        Submit
                      </Button>
                    </Link>
                  ) : (
                    <Button id='submitBtn' disabled variant="primary" onClick={handleEmailSubmit}>
                    Submit
                  </Button>
                  )}
                </Col>
              </Row>
            </Container>
          </Form>
        </Card.Body>
      </Card>
    </>
  );
}
