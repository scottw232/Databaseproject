import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './components/App.js';
import { BrowserRouter } from 'react-router-dom';
import axios from "axios";
//import reportWebVitals from './reportWebVitals';

import 'bootstrap/dist/css/bootstrap.min.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
		<BrowserRouter>
			<App />
		</BrowserRouter>
  </React.StrictMode>
);



function app() {
	const [data, setData] = React.useState();
	const url = "http://127.0.0.1:8080";

	const GetData = () => {
		axios.get(url).then((res) => {
			setData(res.data);
		});
	};

  const url_users = "http://127.0.0.1:8080/users";

	const GetData_users = () => {
		axios.get(url_users).then((res) => {
			setData(res.data);
		});
	};

	return (
		<div>
      <div>8080/users</div>
			{data ? <div>{data[1].name}</div> : <button onClick={GetData_users}>Get Users</button>}
		</div>

	);
}

export default app;

// Show in h1 "Hello World", not react welcome page
// ReactDOM.render(<App />, document.getElementById("root"));

// <h1>Hello World</h1>


