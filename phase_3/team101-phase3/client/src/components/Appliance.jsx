import React, { useState, useEffect } from 'react'
import { Stack, Table, Card, Col, Container, Form, Row, Button} from 'react-bootstrap';
import { Link } from "react-router-dom";
import axios from "axios";
import $ from 'jquery';

export default function Appliance({ insertAplCallBack, addNewData, currData }) {

  const appliances = ['cooker', 'washer', 'dryer', 'tv', 'fridge']

  const [addAppliance, setCurrentForm] = useState(true)
  const [applianceList, setApplianceList] = useState([])
  const [currAppliance, setAppliance] = useState(appliances[0])
  const [manufs, setManufs] = useState([])
  const [applianceID, setApplianceID] = useState(1)



  useEffect(() => {
    const get_Manuf = async () => {
      try {
        let res = await axios.get('/get_all_manufacturers')
        let data = res.data
        console.log(data)
        setManufs(data)
        return data
      } catch(err) {
        window.alert(err.data.message)
      }
    }
    get_Manuf()

  }, [])


  const handleAddAppliance = (e) => {
    let manufSplit = $('#manuf').val().split(' ')
    let temp = applianceList
    let info = {}
    info['appliance_number'] = applianceID
    info['model'] = $('#model').val()
    info['manufacturer'] = manufSplit[1]
    info['manufacturer_id'] = parseInt(manufSplit[0])
    info['type'] = currAppliance
    if (currAppliance === appliances[0]) {
      info['is_oven'] = $('#oven').prop('checked')
      info['is_cooktop'] = $('#cooktop').prop('checked')
      info['cooktop_heat_source'] = $('#cooktopHeat').val()
      let ovenHeatSources = []
      if ($('#gas').prop('checked')) {
        ovenHeatSources.push('gas')
      }
      if ($('#electric').prop('checked')) {
        ovenHeatSources.push('electric')
      }
      if ($('#microwave').prop('checked')) {
        ovenHeatSources.push('microwave')
      }
      info['oven_heat_source'] = ovenHeatSources
      info['oven_type'] = $('#ovenType').val()
    }

    else if (currAppliance === appliances[1]) {
      let washerType = 'top'
      if ($('#frontLoad').prop('checked')) {
        washerType = 'front'
      }
      info['loading_type'] = washerType
    }

    else if (currAppliance === appliances[2]) {
      let dryerHeat = 'gas'
      if ($('#dryerEle').prop('checked')) {
        dryerHeat = 'electric'
      }
      if ($('#dryerNone').prop('checked')) {
        dryerHeat = 'none'
      }
      info['dryer_heat_source'] = dryerHeat
    }

    else if (currAppliance === appliances[3]) {
      info['display_type'] = $('#displayType').val()
      info['display_size'] = parseInt($('#displaySize').val())
      info['max_resolution'] = $('#maxRes').val()
    }

    else if (currAppliance === appliances[4]) {
      info['fridge_type'] = $('#fridgeType').val()
    }
    temp.push(info)
    setApplianceID(applianceID+1)
    setApplianceList(temp)
    setCurrentForm(e)
  }

  const handleAddAplList = () => {
    addNewData("appliances", applianceList)
    insertAplCallBack()
  }

  let aplTypeForm = (<></>)

  //cooker
  if (currAppliance === appliances[0]) {
    aplTypeForm = (
      <Container fluid className='mb-2'>
        <Row className='mb-4'>

          <Col>
            <Form>
              <Form.Check
                type='checkbox'
                id='oven'
                label="Oven"
                className='text-start'
              />
            </ Form>
          </Col>

          <Col>
            <Form>
              <Form.Check
                type='checkbox'
                id='cooktop'
                label='Cooktop'
                className='text-start'
              />
            </ Form>
          </Col>

        </Row>

        <Row>
          <Col>
            <Stack >
              <div className='text-start mb-2'>Heat source:</div>
              <div className='mb-3' style={{borderColor: 'gray', borderStyle: 'solid', borderWidth: 'thin'}}>
                <Form >
                  <div className='m-2'>
                    <Form.Check
                      type='checkbox'
                      id='gas'
                      label='Gas'
                      className='text-start'
                    />
                  </div>
                </ Form>

                <Form >
                  <div className='m-2'>
                    <Form.Check
                      type='checkbox'
                      id='electric'
                      label='Electric'
                      className='text-start'
                    />
                  </div>
                </ Form>
                <Form >
                  <div className='m-2'>
                    <Form.Check
                      type='checkbox'
                      id='microwave'
                      label='Microwave'
                      className='text-start'
                    />
                  </div>

                </ Form>
              </div>
              <div className='text-start mb-2'>
                <Row>
                  <Col>Type:</Col>
                  <Col>
                      <Form.Select id='ovenType' aria-label="Default select example">
                      <option value="convection">Convection</option>
                      <option value="conventional">Conventional</option>
                    </Form.Select></Col>
                </Row>
              </div>
            </Stack>
          </Col>
          <Col>
            <div className='text-start mb-2'>
              <Row>
                <Col>Heat source:</Col>
                <Col>
                  <Form.Select id='cooktopHeat' aria-label="Default select example">
                    <option value="gas">Gas</option>
                    <option value="electric">Electric</option>
                    <option value="radiant">Radiant electric</option>
                    <option value="induction">Induction</option>
                  </Form.Select>
                </Col>
              </Row>
            </div>
          </Col>
        </Row>
      </Container>
    )
  }

  //dryer
  if (currAppliance === appliances[2]) {
    aplTypeForm = (
      <>
        <div className='mb-2'>Heat source:</div>
        <Container fluid className='mb-4'>
          <Row>
            <Form>
              <Form.Check
                inline
                label="Gas"
                name="dryerGroup"
                defaultChecked
                type='radio'
                id='dryerGas'
              />
              <Form.Check
                inline
                label="Electric"
                name="dryerGroup"
                type='radio'
                id='dryerEle'
              />
              <Form.Check
                inline
                label="None"
                name="dryerGroup"
                type='radio'
                id='dryerNone'
              />
            </Form>
          </Row>
        </Container>
      </>
    )
  }

  //washer
  if (currAppliance === appliances[1]) {
    aplTypeForm = (
      <>
        <div className='mb-2'>Loading type:</div>
        <Container fluid className='mb-4'>
          <Row>
            <Form>
              <Form.Check
                inline
                label="Top"
                defaultChecked
                name="washerGroup"
                type='radio'
                id='topLoad'
              />
              <Form.Check
                inline
                label="Front"
                name="washerGroup"
                type='radio'
                id='frontLoad'
              />
            </Form>
          </Row>
        </Container>
      </>
    )
  }

  //fridge
  if (currAppliance === appliances[4]) {
    aplTypeForm = (
      <>
        <Container fluid className='mb-4'>
          <Form className='text-start'>
            <Form.Group className="mb-3" controlId="fridgeType">
              <Row>
                <Col><Form.Label className='mt-2'>Refrigerator/freezer type:</Form.Label></Col>
                <Col xs={10}>
                  <Form.Select aria-label="Default select example">
                    <option value="bottom">Bottom freezer refrigerator</option>
                    <option value="french">French door refrigerator</option>
                    <option value="side">Side-by-side refrigerator</option>
                    <option value="top">Top freezer refrigerator</option>
                    <option value="chest">Chest freezer</option>
                    <option value="upright">Upright freezer</option>
                  </Form.Select>
                </Col>

              </Row>
            </Form.Group>
          </Form>
        </Container>
      </>
    )
  }

  //tv
  if (currAppliance === appliances[3]) {
    aplTypeForm = (
      <Form>
        <Form.Group className="mb-3" controlId="displayType">
          <Container fluid>
            <Row>
              <Col className="text-start">
                <Form.Label className='mt-2'>Display type:</Form.Label>
              </Col>
              <Col xs={10}>
                <Form.Select aria-label="Default select example">
                  <option value="tube">Tube</option>
                  <option value="dlp">DLP</option>
                  <option value="plasma">Plasma</option>
                  <option value="lcd">LCD</option>
                  <option value="led">LED</option>
                </Form.Select>

              </Col>
            </Row>
          </Container>
        </Form.Group>

        <Form.Group className="mb-3" controlId="displaySize">
          <Container fluid>
            <Row>
              <Col className="text-start">
                <Form.Label className='mt-2'>Display size (inches):</Form.Label>
              </Col>
              <Col xs={10}>
              <Form.Control type="float"/>
              </Col>
            </Row>
          </Container>
        </Form.Group>

        <Form.Group className="mb-3" controlId="maxRes">
          <Container fluid>
            <Row>
              <Col className="text-start">
                <Form.Label className='mt-2'>Maximum resolution:</Form.Label>
              </Col>
              <Col xs={10}>
                <Form.Select aria-label="Default select example">
                  <option value="480i">480i</option>
                  <option value="576i">576i</option>
                  <option value="720i">720i</option>
                  <option value="1080i">1080i</option>
                  <option value="1080p">1080p</option>
                  <option value="1440p">1440p</option>
                  <option value="2160p">2160p (4k)</option>
                  <option value="4320p">4320p (8k)</option>
                </Form.Select>

              </Col>
            </Row>
          </Container>
        </Form.Group>
      </Form>
    )
  }

  let currForm = (
    <>
      <div className='mb-4'>Please provide the details for the appliance.</div>

      <Form.Group className="mb-3" controlId="aplType">
        <Container fluid>
          <Row>
            <Col className="text-start">
              <Form.Label className='mt-2'>Appliance Type:</Form.Label>
            </Col>
            <Col xs={10}>
              <Form.Select
                aria-label="Default select example"
                onChange={e => setAppliance(e.target.value)}
              >
                <option value="cooker">Cooker</option>
                <option value="washer">Washer</option>
                <option value="dryer">Dryer</option>
                <option value="tv">TV</option>
                <option value="fridge">Refrigerator/Freezer</option>
              </Form.Select>
            </Col>
          </Row>
        </Container>
      </Form.Group>

      <Form.Group className="mb-3" controlId="manuf">
        <Container fluid>
          <Row>
            <Col className="text-start">
              <Form.Label className='mt-2'>Manufacturer:</Form.Label>
            </Col>
            <Col xs={10}>
              <Form.Select aria-label="Default select example">
                {
                  manufs.map(({ id, manufacturer_name }) => (
                    <option key={id} value={id + ' ' + manufacturer_name}>{manufacturer_name}</option>
                  ))
                }
              </Form.Select>
            </Col>
          </Row>
        </Container>
      </Form.Group>

      <Form.Group className="mb-3" controlId="model">
        <Container fluid>
          <Row>
            <Col className="text-start">
              <Form.Label className='mt-2'>Model Name:</Form.Label>
            </Col>
            <Col xs={10}>
              <Form.Control type="text"/>
            </Col>
          </Row>
        </Container>
      </Form.Group>

      <hr
        style={{color: 'black', backgroundColor: 'black', height: '2px', margin: '25px 15px'}}
      />

      {aplTypeForm}

      <Button size='lg' onClick={() => handleAddAppliance(false)}>
        Add
      </Button>
    </>
  )

  if (!addAppliance) {
    currForm = (
      <>
        <div className='mb-4'>
          You have added the following appliances to your household:
        </div>
        <Table className='mb-0' striped bordered hover>
          <thead>
            <tr>
              <th>Appliance #</th>
              <th>Type</th>
              <th>Manufacturer</th>
              <th>Model</th>
            </tr>
          </thead>
          <tbody>
            {
              applianceList.map(function (e, idx) {
                return (
                  <tr key={idx}>
                    <td>{e.appliance_number}</td>
                    <td>{e.type}</td>
                    <td>{e.manufacturer}</td>
                    <td>{e.model}</td>
                  </tr>
                )
              })
            }
          </tbody>
        </Table>
        <div className='mb-4 text-end'>
          <Link onClick={() => setCurrentForm(true)}>+ Add another appliance</Link>
        </div>
        <Link to='/finished'>
          <Button size='lg' onClick={handleAddAplList}>
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
          <h3 className='m-0'>{addAppliance ? 'Add appliance' : 'Appliances'}</h3>
        </Card.Header>
        <Card.Body className='p-3'>
          {currForm}
        </Card.Body>
      </Card>
    </>

  )
}
