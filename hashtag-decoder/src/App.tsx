import React, { useRef, useState, useEffect } from "react";// , { useState, useEffect }
// import socketIOClient from "socket.io-client";
// const ENDPOINT = "http://127.0.0.1:5000";
import GlobeLayout from "./Layouts/GlobeLayout";
import SearchLayout from "./Layouts/SearchLayout";
import GraphLayout from "./Layouts/GraphLayout";

const App: React.FC = () => {
	return (
		<div className="h-[100vh] bg-cover bg-[url('/layers/background.png')]">
			<div className="absolute z-10 w-[100vw] h-[100vh] p-8">
				<div className="h-full">
					<SearchLayout/>
					{/* 
					<GlobeLayout/>
					<GraphLayout/> */}
				</div>
			</div>
		</div>
	);
}

export default App;


// function App() {
// 	const [response, setResponse] = useState({data:''});
// 	const [hashtag, setHashtag] = useState({data:''});
  
// 	useEffect(() => {
// 	  const socket = socketIOClient(ENDPOINT);
// 	  socket.on("currentStatus", data => {
// 		setResponse(data);
// 	  });
// 	  socket.on('currentSession', data => {
// 		  setHashtag(data);
// 	  });
// 	}, []);
  
  
// 	return (
// 	  <div className="bg-[#040d20] h-[100vh] grid grid-cols-3 content-center">
// 		  <div></div>
// 		  <div className="text-center">
// 			  <h1 className="text-3xl text-gray-200 font-bold">
// 				  {response.data}
// 			  </h1>
// 			  <h1 className="text-3xl text-gray-200 font-bold">
// 				  {hashtag.data}
// 			  </h1>
// 		  </div>
// 		  <div></div>
		
// 	  </div>
// 	);
//   }
  
