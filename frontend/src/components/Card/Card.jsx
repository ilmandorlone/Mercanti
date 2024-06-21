// components/Card/Card.jsx
import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { useCardContext } from '../../context/CardContext';
import colors from '../../utils/colors';
import CardButtons from '../CardButtons/CardButtons';
import './Card.css';

const Card = ({ cardId, colorName, cost, player, level, points }) => {
	const { selectedCard, handleCardClick, handleOutsideClick } = useCardContext();
	const isSelected = selectedCard === cardId;

	const handleClick = (event) => {
		if (!isSelected) {
			event.stopPropagation();
			handleCardClick(cardId);
		}
	};

	useEffect(() => {
		const outsideClickListener = (event) => {
			if (!event.target.closest('.card') && !event.target.closest('.buttons')) {
				handleOutsideClick();
			}
		};

		document.addEventListener('click', outsideClickListener);
		return () => {
			document.removeEventListener('click', outsideClickListener);
		};
	}, [handleOutsideClick]);

	const gradient = colors[colorName] || 'linear-gradient(135deg, #ffffff, #ffffff)';

	const costEntries = Object.entries(cost).filter(([_, value]) => value > 0);
	const rows = [];
	while (costEntries.length) {
		rows.push(costEntries.splice(0, 3));
	}

	const card = { cost };

	return (
		<div
			className={`card ${isSelected ? 'selected' : ''}`}
			style={{ background: gradient }}
			data-card-id={cardId}
			onClick={handleClick}
		>
			<div className="card-cost">
				{rows.reverse().map((row, rowIndex) => (
					<div key={rowIndex} className="cost-row">
						{row.map(([color, value]) => (
							<div key={color} className="token" style={{ background: colors[color] }}>
								{value}
							</div>
						))}
					</div>
				))}
			</div>
			{points > 0 && (
				<div className="card-points">
					<div className="star">
						<span className="points">{points}</span>
					</div>
				</div>
			)}
			{isSelected && <CardButtons cardId={cardId} showPurchase player={player} card={card} level={level} />}
		</div>
	);
};

Card.propTypes = {
	cardId: PropTypes.number.isRequired,
	colorName: PropTypes.string.isRequired,
	cost: PropTypes.objectOf(PropTypes.number).isRequired,
	player: PropTypes.object.isRequired,
	level: PropTypes.number.isRequired,
	points: PropTypes.number.isRequired,
};

export default Card;
