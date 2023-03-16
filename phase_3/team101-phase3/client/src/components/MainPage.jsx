import React from 'react'
import { Button, Card, ListGroup } from 'react-bootstrap';
import { Link } from 'react-router-dom';

export default function MainPage() {
  return (
    <Card border="dark" style={{margin: '1rem 3em'}}>

      <Card.Header style={{background: 'DarkGray'}}>
        <h1>Welcome to Hemkraft!</h1>
        <h3 className='m-0'>Please choose what you'd like to do:</h3>
      </Card.Header>

      <ListGroup variant="flush">
        <ListGroup.Item >
          <Link to='/email'>
            <Button>Enter my household info</Button>
          </Link>
        </ListGroup.Item>
        <ListGroup.Item>
          <Link to='/reports'>
            <Button>View reports/query data</Button>
          </Link>
        </ListGroup.Item>
        <ListGroup.Item>
          <Link to='/avgtvsize'>
            <Button>AvgTVSize</Button>
          </Link>
        </ListGroup.Item>
      </ListGroup>

    </Card>
  )
}
