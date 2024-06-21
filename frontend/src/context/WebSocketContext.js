// src/context/WebSocketContext.js
import React, { createContext, useContext, useEffect, useRef, useState } from 'react';

const WebSocketContext = createContext(null);

const useWebSocket = () => {
	return useContext(WebSocketContext);
};

const WebSocketProvider = ({ children, playerId }) => {
	const [isOpen, setIsOpen] = useState(false);
	const [error, setError] = useState(null);
	const [connectionStatus, setConnectionStatus] = useState('disconnected');
	const socketRef = useRef(null);
	const messageHandlers = useRef([]);

	const connect = (id) => {
		const hostname = window.location.hostname; // Ottieni dinamicamente l'IP/hostname
		setConnectionStatus('connecting');
		socketRef.current = new WebSocket(`ws://${hostname}:3333/ws?playerId=${id}`);

		socketRef.current.onopen = () => {
			console.log('WebSocket connection established');
			setIsOpen(true);
			setConnectionStatus('connected');
		};

		socketRef.current.onmessage = (event) => {
			console.log('Received WebSocket message:', event.data);
			try {
				const data = JSON.parse(event.data);
				messageHandlers.current.forEach(handler => handler(data));
			} catch (error) {
				console.error('Failed to parse message:', event.data);
			}
		};

		socketRef.current.onclose = () => {
			console.log('WebSocket connection closed');
			setIsOpen(false);
			setConnectionStatus('disconnected');
		};

		socketRef.current.onerror = (error) => {
			console.error('WebSocket error:', error);
			setError(error);
			setConnectionStatus('error');
		};
	};

	useEffect(() => {
		if (playerId) {
			connect(playerId);
		}

		return () => {
			if (socketRef.current) {
				socketRef.current.close();
			}
		};
	}, [playerId]);

	const sendMessage = (message) => {
		if (socketRef.current && isOpen) {
			console.log('Sending WebSocket message:', message);
			socketRef.current.send(JSON.stringify(message));
		} else {
			console.error('WebSocket is not open');
		}
	};

	const addMessageHandler = (handler) => {
		messageHandlers.current.push(handler);
	};

	const removeMessageHandler = (handler) => {
		messageHandlers.current = messageHandlers.current.filter(h => h !== handler);
	};

	const retryConnection = () => {
		if (!isOpen && playerId) {
			connect(playerId);
		}
	};

	return (
		<WebSocketContext.Provider value={{ isOpen, sendMessage, error, connectionStatus, retryConnection, addMessageHandler, removeMessageHandler, playerId }}>
			{children}
		</WebSocketContext.Provider>
	);
};

export { WebSocketProvider, useWebSocket };
export default WebSocketContext;
