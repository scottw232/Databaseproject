import React, { useEffect, useReducer, useState } from 'react'
import { Container, Row, Col, Form, Card, Table, Button } from 'react-bootstrap';
import axios from "axios";
import { Link } from 'react-router-dom';

export default function Reports() {

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

  const [reportType, setReportType] = useState(0)
  const [fetchedData, setFetchedData] = useState([])
  const [top25DrilDownData, setTop25DrillDownData] = useState([])
  const [, forceUpdate] = useReducer(x => x +1, 0)

  useEffect(() => {
    const fetchData = async () => {
      try {
        let res = await axios.get(urls[reportType])
        let data = res.data
        setFetchedData([...data])
      } catch(err) {
        window.alert(err.data.message)
      }
    }
    fetchData()
  }, [reportType])



  useEffect(() => {
    console.log(fetchedData)

  }, [fetchedData])


  const handleReportChange = (e) => {
    console.log(e)
    setReportType(e)
    forceUpdate()
  }

  console.log(reportType)
  if (reportType === 0) {
    console.log(fetchedData)
    reportBlock = (

      <>
        <Table className='mb-0' striped bordered hover>
          <thead>
            <tr>
              <th>Manufacturer</th>
              <th>Total # of Appliances</th>
            </tr>
          </thead>
          <tbody>
            {
              fetchedData.map(function (e, idx) {
                return (
                  <tr key={idx}>
                    <td id={e.manufacturer_name} onClick={e => handleTop25DrillDown(e.target.id)}>{e.manufacturer_name}</td>
                    <td>{e.total_appliance_count}</td>
                  </tr>
                )
              })
            }
          </tbody>
        </Table>
        {
          top25DrilDownData.length === 0 ? (<></>) : (
            <div>
              <h3 className='mt-5'>{top25DrilDownData[0].manufacturer_name} Drilldown Report</h3>
              <Table className='mt-3'>
                <thead>
                    <tr>
                      <th>Appliance Type</th>
                      <th>Total # of Appliances For Manufacturer</th>
                    </tr>
                  </thead>
                  <tbody>
                  {
                    top25DrilDownData.map(function (e, idx) {
                      return (
                        <tr key={idx}>
                          <td>{e.appliance_type}</td>
                          <td>{e.total_appliance_count}</td>
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
      </>
    )
  }

  const handleStateDrillDown = async (state) => {

  }

  const handleTop25DrillDown = async (manufName) => {
    try {
      let req = '/get_top_25_manufacturer_drilldown?manufacturer_name=' + manufName
      let res = await axios.get(req)
      setTop25DrillDownData(res.data)
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
        <Container fluid className='mb-4'>
          <Form className='text-start'>
            <Form.Group className="mb-3" controlId="reportType">
              <Row><Form.Label className='mt-2'>
                  Please select a report from the dropdown below:
                </Form.Label>
              </Row>
              <Row>
                <Form.Select onChange={e => handleReportChange(e.target.value)} aria-label="Default select example">
                  <option value={0}>Top 25 Popular Manufacturers</option>
                  <option value={1}>Manufacturer/Model Search</option>
                  <option value={2}>Average TV Display Size by State</option>
                  <option value={3}>Extra Fridge/Freezer Report</option>
                  <option value={4}>Landury Center Report</option>
                  <option value={5}>Bathroom Statistics</option>
                  <option value={6}>Household Averages By Radius</option>
                </Form.Select>
              </Row>
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
