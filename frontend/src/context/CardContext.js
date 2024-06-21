// src/context/CardContext.js
import React, { createContext, useContext, useState, useCallback } from 'react';

const CardContext = createContext();

export const useCardContext = () => {
	return useContext(CardContext);
};

export const CardProvider = ({ children }) => {
	const [selectedCard, setSelectedCard] = useState(null);

	const handleCardClick = useCallback((cardId) => {
		setSelectedCard(cardId);
	}, []);

	const handleOutsideClick = useCallback(() => {
		setSelectedCard(null);
	}, []);

	return (
		<CardContext.Provider value={{ selectedCard, handleCardClick, handleOutsideClick }}>
			{children}
		</CardContext.Provider>
	);
};
