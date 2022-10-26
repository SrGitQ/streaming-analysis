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
	no_users: 140,
	sentiment_timeline: [
		{ positive: 0.33, neutral: 0.53, negative: 0.33 },
	],
	hash_network:{
			nodes: [
				{ id: '#Harry' },
				{ id: '#Sally' },
			],
			links: [
				{ source: '#Harry', target: '#Sally' },
			]
	},
	hashtags: 140,
	places_locations:[
		{ lat: 21.009293505988, lng: -89.69595640433737},
	]
}

const ENDPOINT = "http://127.0.0.1:5000";

const StreamRunner: React.FC = () => {

	const [mode, setMode] = useState("globe");
	const [response, setResponse] = useState(data);
	const [network, setNetwork] = useState({nodes:[], links:[]});



	useEffect(() => {
		const socket = socketIOClient(ENDPOINT);
		socket.on("currentStatus", data_current => {
		  	setResponse(data_current);
			  setResponse(data_current);
			  if (data_current.hash_network.nodes.length > network.nodes.length){
	  
				  setNetwork({
					  nodes: response.hash_network.nodes as any,
					  links: response.hash_network.links as any
				  });
			  }
		

		});
		socket.on('currentSession', data_current => {
			setResponse(data_current);
			if (data_current.hash_network.nodes.length > network.nodes.length){
	
				setNetwork({
					nodes: response.hash_network.nodes as any,
					links: response.hash_network.links as any
				});
			}
		});
	  }, []);


	return (
		<div>
			{mode === "globe" ? <GlobeLayout changeLayout={setMode} data={response}/> : null}
			{mode === "graph" ? <GraphLayout changeLayout={setMode} data={response} network = {network}/> : null}
		</div>
	);
};

const App: React.FC = () => {
	
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
