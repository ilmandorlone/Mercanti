// src/components/CardRow/CardRow.jsx
import React from 'react';
import PropTypes from 'prop-types';
import Card from '../Card/Card';
import CardBack from '../CardBack/CardBack';
import './CardRow.css';

const CardRow = ({ level, rowIndex, cards, remainingCards, player }) => {
	return (
		<div className="card-row">
			<CardBack level={level} cardId={`back-${level}-${rowIndex}`} remainingCards={remainingCards} player={player} />
			{cards.map(card => (
				<Card
					key={card.id}
					cardId={card.id}
					colorName={card.colorName}
					cost={card.cost.reduce((acc, { color, count }) => {
						acc[color] = count;
						return acc;
					}, {})}
					player={player}
					level={level}
					points={card.points}
				/>
			))}
		</div>
	);
};

CardRow.propTypes = {
	level: PropTypes.number.isRequired,
	rowIndex: PropTypes.number.isRequired,
	cards: PropTypes.arrayOf(
		PropTypes.shape({
			id: PropTypes.number.isRequired,
			level: PropTypes.number.isRequired,
			color: PropTypes.string.isRequired,
			cost: PropTypes.arrayOf(
				PropTypes.shape({
					color: PropTypes.string.isRequired,
					count: PropTypes.number.isRequired,
				})
			).isRequired,
			points: PropTypes.number.isRequired,
		})
	).isRequired,
	remainingCards: PropTypes.number.isRequired,
	player: PropTypes.object.isRequired,
};

export default CardRow;
