import React, { useState, useEffect } from "react";// , { useState, useEffect }
import socketIOClient from "socket.io-client";
import GlobeLayout from "./Layouts/GlobeLayout";
import SearchLayout from "./Layouts/SearchLayout";
import GraphLayout from "./Layouts/GraphLayout";
import {
	Route,
  	Routes,
	BrowserRouter,
} from "react-router-dom";

const data = {
	hashtag: "hashtag",
	tweets: 140,
	users: 140,
	mentions: 13,
	places: 13,
	verified: 13,
	sentiment: {
		positive: 0.60,
		neutral: 0.20,
		negative: 0.20,
	},
	devices: {
		android: 33,
		ios: 33,
		web: 33,
	},
	sentiment_timeline: [
		{ positive: 0.33, neutral: 0.53, negative: 0.33 },
		{ positive: 0.3, neutral: 0.53, negative: 0.33 },
		{ positive: 0.23, neutral: 0.33, negative: 0.60 },
		{ positive: 0.12, neutral: 0.33, negative: 0.33 },
		{ positive: 0.6, neutral: 0.20, negative: 0.20 },
	],
	hash_network:{
			nodes: [
				{ id: '#Harry' },
				{ id: '#Sally' },
				{ id: '#Alice' },
				{ id: '#Bob' },
			],
			links: [
				{ source: '#Harry', target: '#Sally' },
				{ source: '#Harry', target: '#Alice' },
				{ source: '#Harry', target: '#Bob' },
			]
	},
	hashtags: 140,
	places_locations:[
		{ lat: 21.009293505988, lng: -89.69595640433737},
		{ lat: 20.009293505988, lng: -88.69595640433737},
		{ lat: 19.009293505988, lng: -87.69595640433737},
		{ lat: 18.009293505988, lng: -86.69595640433737},

	]
}

type StreamProps = {
	status: typeof data;
}
const ENDPOINT = "http://127.0.0.1:5000";

const StreamRunner: React.FC = () => {
	const [mode, setMode] = useState("globe");
	const [response, setResponse] = useState(data);
	const [hashtag, setHashtag] = useState(data);


	useEffect(() => {
		const socket = socketIOClient(ENDPOINT);
		socket.on("currentStatus", data => {
		  setResponse(data);
		});
		socket.on('currentSession', data => {
			setHashtag(data);
		});
		console.log(response);
	  }, []);

	return (
		<div>
			{mode === "globe" ? <GlobeLayout changeLayout={setMode} data={hashtag}/> : null}
			{mode === "graph" ? <GraphLayout changeLayout={setMode} data={hashtag}/> : null}
		</div>
	);
};

const App: React.FC = () => {
	const [mode, setMode] = useState("search");
	
	return (
		<div className="h-[100vh] bg-cover bg-[url('/layers/background.png')]">
			<div className="absolute z-10 w-[100vw] h-[100vh] p-8">
				<div className="h-full">
					<BrowserRouter>
						<Routes>
							<Route path="/" element={<SearchLayout/>} />
							<Route path="/stream" element={<StreamRunner/>} />
						</Routes>
					</BrowserRouter>
					
				</div>
			</div>
		</div>
	);
}

export default App;

/*
 function App() {
 	const [response, setResponse] = useState({data:''});
 	const [hashtag, setHashtag] = useState({data:''});
  
 	useEffect(() => {
 	  const socket = socketIOClient(ENDPOINT);
 	  socket.on("currentStatus", data => {
 		setResponse(data);
 	  });
 	  socket.on('currentSession', data => {
 		  setHashtag(data);
 	  });
 	}, []);
  
  
 	return (
 	  <div className="bg-[#040d20] h-[100vh] grid grid-cols-3 content-center">
 		  <div></div>
 		  <div className="text-center">
 			  <h1 className="text-3xl text-gray-200 font-bold">
 				  {response.data}
 			  </h1>
 			  <h1 className="text-3xl text-gray-200 font-bold">
 				  {hashtag.data}
 			  </h1>
 		  </div>
 		  <div></div>
		
 	  </div>
 	);
   }
  
*/
