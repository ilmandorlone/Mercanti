// src/components/CardBack/CardBack.jsx
import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { useCardContext } from '../../context/CardContext';
import CardButtons from '../CardButtons/CardButtons';
import './CardBack.css';

const CardBack = ({ cardId, level, remainingCards, player }) => {
	const { selectedCard, handleCardClick, handleOutsideClick } = useCardContext();
	const isSelected = selectedCard === cardId;

	const handleClick = (event) => {
		if (!isSelected && remainingCards > 0) {
			event.stopPropagation();
			handleCardClick(cardId);
		}
	};

	useEffect(() => {
		const outsideClickListener = (event) => {
			if (!event.target.closest('.card-back') && !event.target.closest('.buttons')) {
				handleOutsideClick();
			}
		};

		document.addEventListener('click', outsideClickListener);
		return () => {
			document.removeEventListener('click', outsideClickListener);
		};
	}, [handleOutsideClick]);

	const levels = ['I', 'II', 'III'];
	const colors = ['#D2B48C', '#A0522D', '#5B341B']; // Marroncino chiaro a scuro

	const cardStyle = {
		background: remainingCards > 0 ? colors[level - 1] : 'transparent',
		cursor: remainingCards > 0 ? 'pointer' : 'default',
		opacity: remainingCards > 0 ? 1 : 0.5,
	};

	return (
		<div
			className={`card-back ${isSelected ? 'selected' : ''}`}
			style={cardStyle}
			data-card-id={cardId}
			onClick={handleClick}
		>
			{remainingCards > 0 ? levels[level - 1] : ''}
			{isSelected && <CardButtons cardId={null} showPurchase={false} player={player} card={{}} level={level} />}
		</div>
	);
};

CardBack.propTypes = {
	cardId: PropTypes.string.isRequired,
	level: PropTypes.number.isRequired,
	remainingCards: PropTypes.number.isRequired,
	player: PropTypes.object.isRequired,
};

export default CardBack;
