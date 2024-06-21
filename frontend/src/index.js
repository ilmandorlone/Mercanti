import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route, useSearchParams } from 'react-router-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { WebSocketProvider, useWebSocket } from './context/WebSocketContext';
import { CardProvider } from './context/CardContext';
import { GameProvider } from './context/GameContext';

const AppWithProviders = () => {
	const [searchParams] = useSearchParams();
	const playerId = Number(searchParams.get('id'));

	return (
		<WebSocketProvider playerId={playerId}>
			<CardProvider>
				<GameContextWrapper playerId={playerId}>
					<App />
				</GameContextWrapper>
			</CardProvider>
		</WebSocketProvider>
	);
};

const GameContextWrapper = ({ playerId, children }) => {
	const { sendMessage } = useWebSocket();

	return (
		<GameProvider playerId={playerId} sendMessage={sendMessage}>
			{children}
		</GameProvider>
	);
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
	<React.StrictMode>
		<Router>
			<Routes>
				<Route path="/" element={<AppWithProviders />} />
			</Routes>
		</Router>
	</React.StrictMode>
);

reportWebVitals();
