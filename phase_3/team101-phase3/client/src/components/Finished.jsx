import React from 'react'
import { Card } from 'react-bootstrap';

import { Link } from "react-router-dom";

export default function Finished({ returnToMain, currData }) {
  return (
    <>
      <Card border="dark" style={{margin: '1rem 3em'}}>
        <Card.Header style={{background: 'DarkGray' }}>
          <h3 className='m-0'>Submission complete!</h3>
        </Card.Header>
        <Card.Body className='p-3'>
          <div>Thank you for providing your information to Hemkraft!</div>
          <Link to='/' onClick={(e) => returnToMain}>Return to the main menu</Link>
        </Card.Body>
      </Card>
    </>
  )
}
