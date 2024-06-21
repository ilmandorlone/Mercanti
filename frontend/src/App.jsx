// src/App.jsx
import React from 'react';
import { useLocation } from 'react-router-dom';
import WebSocketTest from './components/WebSocketTest/WebSocketTest';

function App() {
	const location = useLocation();
	const query = new URLSearchParams(location.search);
	const playerId = query.get('id');

	console.log('Player ID:', playerId); // Debug

	return (
		<div>
			<WebSocketTest />
		</div>
	);
}

export default App;
