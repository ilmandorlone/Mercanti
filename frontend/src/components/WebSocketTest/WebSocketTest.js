import React, { useEffect } from 'react';
import { useWebSocket } from '../../context/WebSocketContext';
import { useGameContext } from '../../context/GameContext';
import GridLayout from '../GridLayout/GridLayout';
import GameStateModel from '../../models/GameStateModel';

const WebSocketTest = () => {
	const { playerId, isOpen, sendMessage, error, connectionStatus, retryConnection, addMessageHandler, removeMessageHandler } = useWebSocket();
	const { updateGameState } = useGameContext();

	useEffect(() => {
		const handleWebSocketMessage = (data) => {
			console.log("Received WebSocket message in WebSocketTest:", data);

			const gameState = new GameStateModel(
				data.opponents,
				data.player,
				data.remaining_cards,
				data.tokens,
				data.visible_level1,
				data.visible_level2,
				data.visible_level3,
				data.tempTokens = { 'violet': 0, 'blue': 0, 'green': 0, 'red': 0, 'black': 0, 'gold': 0 },
				data.visible_passengers
			);

			updateGameState(gameState); // Aggiorna il gameState globale
		};

		addMessageHandler(handleWebSocketMessage);

		return () => {
			removeMessageHandler(handleWebSocketMessage);
		};
	}, [addMessageHandler, removeMessageHandler, updateGameState]);

	useEffect(() => {
		if (isOpen) {
			sendMessage({ action: 'get_game_state', player_id: playerId });
		}
	}, [isOpen, sendMessage, playerId]);

	return (
		<div>
			{connectionStatus === 'disconnected' && (
				<div className="center-content">
					<p>Connection is not established. Please click the button to connect.</p>
					<button onClick={retryConnection}>Connect</button>
				</div>
			)}
			{connectionStatus === 'connecting' && <div className="center-content"><p>Connecting to server...</p></div>}
			{connectionStatus === 'connected' && <GridLayout />}
			{connectionStatus === 'error' && (
				<div className="center-content">
					<p>Error occurred: {error?.message}</p>
					<button onClick={retryConnection}>Retry Connection</button>
				</div>
			)}
		</div>
	);
};

export default WebSocketTest;
