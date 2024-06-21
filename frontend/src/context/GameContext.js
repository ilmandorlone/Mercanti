import React, { createContext, useContext, useState, useCallback } from 'react';
import GameStateModel from '../models/GameStateModel';

const GameContext = createContext();

export const useGameContext = () => {
	return useContext(GameContext);
};

export const GameProvider = ({ children, playerId, sendMessage }) => {
	const [gameState, setGameState] = useState(new GameStateModel());
	const [selectedTokens, setSelectedTokens] = useState([]);
	const [moveType, setMoveType] = useState(null);

	const updateTokens = (color, delta) => {
		setGameState(prevState => {
			const newTokens = prevState.tokens.map(token => {
				if (token.color === color) {
					return { ...token, count: token.count + delta };
				}
				return token;
			});
			prevState.tempTokens[color] = prevState.tempTokens[color] - delta;
			const newState = { ...prevState, tokens: newTokens };
			return newState;
		});
	};

	const addToken = (color) => {
		if (color === 'gold') return; // Non permette la selezione dei gettoni d'oro

		// Calcola il numero totale di gettoni posseduti dal giocatore
		const totalTokens = Object.values(gameState.player.tokens).reduce((sum, token) => sum + token.count, 0) + selectedTokens.length;

		// Verifica se il numero totale di gettoni è inferiore a 10
		if (totalTokens >= 10) {
			console.log('Non puoi selezionare più di 10 gettoni in totale.');
			return;
		}

		const token = gameState.tokens.find(token => token.color === color);
		const availableTokens = token ? token.count : 0;
		if (availableTokens <= 0) return; // Verifica che ci siano token disponibili

		// Selezione del primo gettone
		if (selectedTokens.length === 0) {
			setSelectedTokens([color]);
			updateTokens(color, -1);
			return;
		}

		// Selezione del secondo gettone
		if (selectedTokens.length === 1) {
			if (selectedTokens[0] === color && availableTokens >= 3) {
				// Due gettoni dello stesso colore
				setMoveType('twoSame');
				setSelectedTokens([...selectedTokens, color]);
				updateTokens(color, -1);
			} else if (selectedTokens[0] !== color) {
				// Due gettoni di colori diversi
				setMoveType('threeDifferent');
				setSelectedTokens([...selectedTokens, color]);
				updateTokens(color, -1);
			}
			return;
		}

		// Selezione del terzo gettone (solo per tre colori diversi)
		if (moveType === 'threeDifferent' && selectedTokens.length < 3 && !selectedTokens.includes(color)) {
			setSelectedTokens([...selectedTokens, color]);
			updateTokens(color, -1);
		}
	};

	const removeToken = (color) => {
		const index = selectedTokens.indexOf(color);
		if (index !== -1) {
			setSelectedTokens(prevTokens => {
				const newTokens = [...prevTokens];
				newTokens.splice(index, 1);
				return newTokens;
			});
			updateTokens(color, 1);
			if (selectedTokens.length === 2) {
				setMoveType(null);
			}
		}
	};

	const endTurn = () => {
		const tokens = selectedTokens.map(color => ({
			color,
			count: 1,
			action: 'buy'
		}));

		const message = {
			action: 'select_token',
			player_id: playerId,
			tokens
		};

		sendMessage(message);

		setSelectedTokens([]);
		setMoveType(null);
		// Logica per gestire la fine del turno
	};

	return (
		<GameContext.Provider value={{ gameState, addToken, removeToken, selectedTokens, endTurn, updateGameState: setGameState }}>
			{children}
		</GameContext.Provider>
	);
};
