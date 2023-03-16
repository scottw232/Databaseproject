import React, { useEffect, useReducer, useState } from 'react'
import { Container, Row, Col, Form, Card, Table, Button } from 'react-bootstrap';
import axios from "axios";
import { Link } from 'react-router-dom';
import $ from 'jquery';

export default function AvgTVSize() {

  const urls = [
    '/get_top_25_manufacturers',
    '/manufacturer_model_search',
    '/avg_tv_size',
    '/extra_fridges',
    '/extra_fridges',
    '/bathrooms',
    '/household_radius'
  ]

  let reportBlock = (<></>)

  const [reportType, setReportType] = useState(2)
  const [fetchedData, setFetchedData] = useState([])
  const [stateDownData, setStateDownData] = useState([])
  const [, forceUpdate] = useReducer(x => x +1, 0)

  useEffect(() => {
    const fetchData = async () => {
      try {
        let res = await axios.get(urls[reportType])
        let data = res.data
        setFetchedData(data)
      } catch(err) {
        window.alert(err.data.message)
      }
    }
    fetchData()
  }, [reportType])

  useEffect(() => {
    console.log('x')

  }, [fetchedData])

  if (reportType === 2) {
    console.log(fetchedData)
    reportBlock = (
      <>
        <Table className='mb-0' striped bordered hover>
          <thead>
            <tr>
              <th>State</th>
              <th>Average TV Display Size</th>
            </tr>
          </thead>
          <tbody>
            {
              fetchedData.map(function (e, idx) {
                return (
                  <tr key={idx}>
                    <td id={e.state} onClick={e => handleStateDrillDown(e.target.id)}>{e.state}</td>
                    <td>{e.average_tv_size}</td>
                  </tr>
                )
              })
            }
          </tbody>
        </Table>
        {
          stateDownData.length === 0 ? (<></>) : (
            <div>
              <h3 className='mt-5'>{stateDownData[0].state} Drilldown Report</h3>
              <Table className='mt-3'>
                <thead>
                    <tr>
                      <th>Display Type</th>
                      <th>Max Resolution</th>
                      <th>Average TV Size</th>
                    </tr>
                  </thead>
                  <tbody>
                  {
                    stateDownData.map(function (e, idx) {
                      return (
                        <tr key={idx}>
                          <td>{e.display_type}</td>
                          <td>{e.max_resolution}</td>
                          <td>{e.average_tv_size}</td>
                        </tr>
                      )
                    })
                  }
                </tbody>
              </Table>
            </div>
          )
        }
      </>
    )
  }

  const handleStateDrillDown = async (state) => {
    try {
      let req = '/avg_tv_size?state=' + state
      let res = await axios.get(req)
      setStateDownData(res.data)
    } catch(err) {
      window.alert(err.data.message)
    }
  }



  return (
    <Card border="dark" style={{margin: '1rem 3em'}}>

      <Card.Header style={{background: 'DarkGray'}}>
        <h1>View reports/query data</h1>
      </Card.Header>
      <Card.Body>
        <div>
        <Form >
          <Form.Group className="mb-3 text-start" controlId="state">
            <Form.Label>Please enter the state initials</Form.Label>
            <Form.Control type="text" placeholder="GA" />
          </Form.Group>
          <Button variant="primary" onClick={e => handleStateDrillDown($('#state').val())}>
            Submit
          </Button>
        </Form>
        </div>
        <Container fluid className='mb-4'>
          <Form className='text-start'>
            <Form.Group className="mb-3" controlId="reportType">
            </Form.Group>
          </Form>
        </Container>
        <div>
          {reportBlock}
        </div>
      </Card.Body>

    </Card>

  )
}
