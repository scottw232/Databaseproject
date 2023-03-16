import '../App.css';
import Finished from "./Finished.jsx";
import Email from "./Email.jsx";
import Postal from "./Postal.jsx";
import Household from "./Household.jsx";
import Bathroom from "./Bathroom.jsx";
import Appliance from "./Appliance.jsx";
import Reports from './Reports.jsx';
import { useState, useEffect } from 'react';
import { Routes, Route, Link } from "react-router-dom";
import MainPage from './MainPage.jsx';
import AvgTVSize from './AvgTVSize.jsx';
import axios from "axios";


axios.defaults.baseURL = "http://localhost:8080"

function App() {

  let currData = {}

  //const [currData, setCurrData] = useState([])

  const [isMainPage, setCurrentPage] = useState(true)

  const [test, setTest] = useState(null)

  const testBackEnd = async () => {
    try {
      let res = await axios.get('/ingest_sample_data')
      let result = res.data
      console.log(result.message)
      setTest(result.message)

    } catch(err) {
      console.log(err)
    }
  }

  useEffect(() => {
    testBackEnd()
  }, [])


  const handleNewData = (name, data) => {
    currData[name] = data
  }

  const buttonHandler = (e) => {
    setCurrentPage(false)
  }

  const handleFinished = (e) => {
    setCurrentPage(true)
  }

  const insertAppliances = async () => {
    let aplList = currData['appliances']
    let email = currData['email']
    for (let i = 0; i < aplList.length; i++) {
      await insertAplBase(aplList[i], email)
      if (aplList[i]['type'] == 'cooker') {
        if (aplList[i]['is_oven']) {
          await insertOven(aplList[i], email)
          await insertOvenHS(aplList[i], email)
        }
        if (aplList[i]['is_cooktop']) {
          await insertCookTop(aplList[i], email)
        }
      }
      else if (aplList[i]['type'] == 'washer') {
        await insertWasher(aplList[i], email)
      }
      else if (aplList[i]['type'] == 'dryer') {
        await insertDryer(aplList[i], email)
      }
      else if (aplList[i]['type'] == 'tv') {
        await insertTV(aplList[i], email)
      }
      else if (aplList[i]['type'] == 'fridge') {
        await insertFridge(aplList[i], email)
      }
    }
  }

  const insertAplBase = async (apl, email) => {
    let req = '/insert_appliance?model=' + apl.model + '&manufacturer_id=' +
                apl.manufacturer_id + '&email=' + email + '&appliance_type=' +
                apl.type
    try {
      let res = await axios.post(req)
      let result = res.data
      return result
    } catch (error) {
      window.alert(err.response.data.message)
    }
  }

  const insertOven = async (apl, email) => {
    let req = '/insert_oven?oven_type=' + apl.oven_type + '&appliance_number=' +
                apl.appliance_number + '&email=' + email
    try {
      let res = await axios.post(req)
      let result = res.data
      console.log('Oven success')
      return result
    } catch (error) {
      window.alert(err.response.data.message)
    }
  }

  const insertOvenHS = async (apl, email) => {
    let heatSources = ''
    for (let i = 0; i < apl.oven_heat_source.length; i++) {
      heatSources = heatSources + apl.oven_heat_source[i] + ','
    }
    let req = '/insert_oven_heat_source?oven_heat_source=' + heatSources.slice(0, -1) +
                '&appliance_number=' + apl.appliance_number + '&email=' + email
    try {
      let res = await axios.post(req)
      let result = res.data
      console.log('OvenHS success')
      return result
    } catch (error) {
      window.alert(err.response.data.message)
    }
  }

  const insertCookTop = async (apl, email) => {
    let req = '/insert_cooktop?cooktop_heat_source=' + apl.cooktop_heat_source +
                '&appliance_number=' + apl.appliance_number + '&email=' + email
    try {
      let res = await axios.post(req)
      let result = res.data
      console.log('CTop success')
      return result
    } catch (error) {
      window.alert(err.response.data.message)
    }
  }

  const insertWasher = async (apl, email) => {
    let req = '/insert_washer?loading_type=' + apl.loading_type + '&appliance_number=' +
                apl.appliance_number + '&email=' + email
    try {
      let res = await axios.post(req)
      let result = res.data
      console.log('Washer success')
      return result
    } catch (error) {
      window.alert(err.response.data.message)
    }
  }

  const insertDryer = async (apl, email) => {
    let req = '/insert_dryer?dryer_heat_source=' + apl.dryer_heat_source +
                '&appliance_number=' + apl.appliance_number + '&email=' + email
    try {
      let res = await axios.post(req)
      let result = res.data
      console.log('Dryer success')
      return result
    } catch (error) {
      window.alert(err.response.data.message)
    }
  }

  const insertTV = async (apl, email) => {
    let req = '/insert_tv?display_type=' + apl.display_type + '&display_size='
                + apl.display_size + '&max_resolution=' + apl.max_resolution +
                '&appliance_number=' + apl.appliance_number + '&email=' + email
    try {
      let res = await axios.post(req)
      let result = res.data
      console.log('TV success')
      return result
    } catch (error) {
      window.alert(err.response.data.message)
    }
  }

  const insertFridge = async (apl, email) => {
    let req = '/insert_fridge?fridge_type=' + apl.fridge_type + '&appliance_number=' +
                apl.appliance_number + '&email=' + email
    try {
      let res = await axios.post(req)
      let result = res.data
      console.log('Fridge success')
      return result
    } catch (error) {
      window.alert(err.response.data.message)
    }
  }

  const insertHouseData = async () => {
    console.log(currData['phone'])
    await insertHousehold()
    if (currData['phone'] !== 'none') {
      await insertPhone()
    }
  }

  const insertBathrooms = async () => {
    let bathroomList = currData['bathrooms']
    for (let i = 0; i < bathroomList.length; i++) {
      if (bathroomList[i]['type'] === 'full') {
        await insertFullBath(bathroomList[i])
      }
      if (bathroomList[i]['type'] === 'half') {
        await insertHalfBath(bathroomList[i])
      }
    }
  }

  const insertFullBath = async (bathroom) => {
    let req = '/insert_full_bathroom?email=' + currData['email'] +
                '&number_of_sinks=' + bathroom.number_of_sinks +
                '&number_of_commodes=' + bathroom.number_of_commodes +
                '&number_of_bidets=' + bathroom.number_of_bidets +
                '&number_of_bathtubs=' + bathroom.number_of_bathtubs +
                '&number_of_showers=' + bathroom.number_of_showers +
                '&number_of_tub_showers=' + bathroom.number_of_tub_showers +
                '&is_primary_bathroom=' + bathroom.is_primary_bathroom
    try {
      let res = await axios.post(req)
      console.log('Fullbath Success')
    } catch(err) {
      window.alert(err.response.data.message)
    }
  }

  const insertHalfBath = async (bathroom) => {
    let req = '/insert_half_bathroom?email=' + currData['email'] +
                '&number_of_sinks=' + bathroom.number_of_sinks +
                '&number_of_commodes=' + bathroom.number_of_commodes +
                '&number_of_bidets=' + bathroom.number_of_bidets +
                '&half_bath_name=placeholder'
    try {
      let res = await axios.post(req)
      console.log('Halfbath Success')
    } catch(err) {
      window.alert(err.response.data.message)
    }
  }

  const insertHousehold = async () => {
    let req = '/insert_household?email=' + currData['email'] + '&square_footage=' +
                currData['household'].square_footage + '&number_of_occupants=' +
                currData['household'].number_of_occupants + '&number_of_bedrooms=' +
                currData['household'].number_of_bedrooms + '&household_type=' +
                currData['household'].household_type + '&postal_code=' + currData['postal'].postal_code
    try {
      let res = await axios.post(req)
      console.log('Household success')
    } catch(err) {
      window.alert(err.response.data.message)
    }
  }

  const insertPhone = async () => {
    let req = '/insert_phone_number?area_code=' + currData['phone'].area_code +
                '&seven_digits=' + currData['phone'].phone_number +
                '&phone_type=' + currData['phone'].phone_type +
                '&email=' + currData['email']
    try {
      let res = await axios.post(req)
      console.log('Phone success')
    } catch(err) {
      window.alert(err.response.data.message)
    }
  }

  // let mainPage = (
  //   <>
  //     <Card  border="dark" className='m-3'>

  //       <Card.Header style={{background: 'DarkGray'}}>
  //         <h1>Welcome to Hemkraft!</h1>
  //         <h3 className='m-0'>Please choose what you'd like to do:</h3>
  //       </Card.Header>

  //       <ListGroup variant="flush">
  //         <ListGroup.Item >
  //           <Link to='/email'>
  //             <Button onClick={buttonHandler}>Enter my household info</Button>
  //           </Link>
  //         </ListGroup.Item>
  //         <ListGroup.Item>View reports/query data</ListGroup.Item>
  //       </ListGroup>

  //     </Card>
  //     {test}
  //   </>

  // )

  // if (!isMainPage) {
  //   mainPage = (
  //     <>
  //     </>
  //   )
  // }

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<MainPage/>}></Route>
        <Route path="/email" element={<Email addNewData={handleNewData} currData={currData}/>}></Route>
        <Route path="/postal" element={<Postal addNewData={handleNewData} currData={currData}/>}></Route>
        <Route path="/household" element={<Household insertHouseCallback={insertHouseData} addNewData={handleNewData} currData={currData}/>}></Route>
        <Route path="/bathroom" element={<Bathroom insertBathrmCallback={insertBathrooms} addNewData={handleNewData} currData={currData}/>}></Route>
        <Route path="/appliance" element={<Appliance insertAplCallBack={insertAppliances} addNewData={handleNewData} currData={currData}/>}></Route>
        <Route path="/finished" element={<Finished returnToMain={handleFinished} currData={currData}/>}></Route>
        <Route path="/reports" element={<Reports/>}></Route>
        <Route path="/avgtvsize" element={<AvgTVSize/>}></Route>
      </Routes>
    </div>

  );
}

export default App;
