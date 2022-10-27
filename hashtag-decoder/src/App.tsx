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
import { collapseTextChangeRangesAcrossMultipleVersions } from "typescript";

const data_test = {
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
			],
			links: [
				
			]
	},
	hashtags: 140,
	places_locations:[
		{ lat: 21.009293505988, lng: -89.69595640433737},
	]
}

type Props = {
	data: any,
	network: any,
}

const StreamRunner: React.FC<Props> = ({data, network}) => {
	const [mode, setMode] = useState("globe");

	// useEffect(() => {
	// 	let inside = true
	// 	data.hash_network.nodes.forEach((node:any) => {
	// 		network.nodes.forEach((node_current:any) => {
	// 			if(node_current.id === node.id){
	// 				console.log('flas')
	// 				inside = true
	// 			}
	// 		});
	// 		if(!inside){
	// 			// @ts-ignore
	// 			network.nodes.push(node)
	// 		}
	// 	});
	// 	data.hash_network.links.forEach((link:any) => {
	// 		// @ts-ignore
	// 		if (!network.links.includes(link)) {
	// 			// @ts-ignore
	// 			network.links.push(link)
	// 		}
	// 	});
	// }, []);

	return (
		// <GraphLayout changeLayout={setMode} data={data} network = {network}/>
		<div>
			{mode === "globe" ? <GlobeLayout changeLayout={setMode} data={data}/> : null}
			{mode === "graph" ? <GraphLayout changeLayout={setMode} data={data} network = {network}/> : null}
		</div>
	);
};

const App: React.FC = () => {
	const interval = 4000;
	const [response, setResponse] = useState(data_test);

	// async function check() {
	// 	const res = await fetch('http://127.0.0.1:5000/streamdata');
	// 	const data = await res.json();
	// 	setResponse(data);
	// 	let new_size = data.hash_network.nodes.length
	// 	let last_size = network.nodes.length
	// 	if(new_size > last_size){
	// 		for(let i = new_size-1; i > last_size-1; i--){
	// 			setNetwork({
	// 				nodes: [...network.nodes, data.hash_network.nodes[i]],
	// 				links: network.links
	// 			})
	// 		}
	// 	}
	// 	new_size = data.hash_network.links.length
	// 	last_size = network.links.length
	// 	if(new_size > last_size){
	// 		for(let i = new_size-1; i > last_size-1; i--){
	// 			setNetwork({
	// 				nodes: network.nodes,
	// 				links: [...network.links, data.hash_network.links[i]]
	// 			})
	// 		}
	// 	}
		
	// 	// console.log(response, network)
	// }

	// useEffect(() => {
	// 	check();
	// }, []);

	// setTimeout(async () => {
	// 	check();

	// }, interval);
	const getData = async () => {
		const res = await fetch('http://127.0.0.1:5000/streamdata');
		const data = await res.json() as typeof data_test;
		if(!data.hash_network.nodes.includes({id: data.hashtag})){
			data.hash_network.nodes.push({id: data.hashtag})
		}

		// let new_size_nodes = data.hash_network.nodes.length
		// let last_size_nodes = network.nodes.length
		// let new_size_links = data.hash_network.links.length
		// let last_size_links = network.links.length
		// setNetwork(({nodes, links}) => {
		// 	if(new_size_nodes > last_size_nodes){
		// 		nodes = [...nodes, ...data.hash_network.nodes.slice(last_size_nodes, new_size_nodes)]
		// 	}
		// 	if(new_size_links > last_size_links){
		// 		links = [...links, ...data.hash_network.links.slice(last_size_links, new_size_links)]
		// 	}
		// 	console.log({nodes, links})
		// 	return {nodes:nodes, links:links}
		// })
		
		// new_size = data.hash_network.links.length
		// last_size = network.links.length
		// if(new_size > last_size){
		// 	for(let i = new_size-1; i > last_size-1; i--){
		// 		setNetwork({
		// 			nodes: network.nodes,
		// 			links: [...network.links, data.hash_network.links[i]]
		// 		})
		// 	}
		// }


		setResponse(data);
	}

	useEffect(() => {
		getData();
	}, []);
	setTimeout(() => {getData()}, interval);
	
	return (
		<div className="h-[100vh] bg-cover bg-[url('/layers/background.png')]">
			<div className="absolute z-10 w-[100vw] h-[100vh] p-8">
				<div className="h-full">
					<BrowserRouter>
						<Routes>
							<Route path="/" element={<SearchLayout/>} />
							<Route path="/stream" element={<StreamRunner data={response} network={response.hash_network}/>}/>
						</Routes>
					</BrowserRouter>
					
				</div>
			</div>
		</div>
	);
}

export default App;
