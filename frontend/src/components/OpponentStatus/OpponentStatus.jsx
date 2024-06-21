// src/components/OpponentStatus/OpponentStatus.jsx
import React from 'react';
import PropTypes from 'prop-types';
import colors from '../../utils/colors';
import './OpponentStatus.css';

const defaultTokens = [
	{ color: 'violet', count: 0 },
	{ color: 'blue', count: 0 },
	{ color: 'green', count: 0 },
	{ color: 'red', count: 0 },
	{ color: 'black', count: 0 },
	{ color: 'gold', count: 0 },
];

const defaultCards = [
	{ color: 'violet', count: 0 },
	{ color: 'blue', count: 0 },
	{ color: 'green', count: 0 },
	{ color: 'red', count: 0 },
	{ color: 'black', count: 0 },
];

const addDefaultTokens = (tokens) => {
	const tokenMap = tokens.reduce((acc, token) => {
		acc[token.color] = token.count;
		return acc;
	}, {});

	return defaultTokens.map((token) => ({
		color: token.color,
		count: tokenMap[token.color] || token.count,
	}));
};

const addDefaultCards = (cards) => {
	const cardMap = cards.reduce((acc, card) => {
		acc[card.color] = card.count;
		return acc;
	}, {});

	return defaultCards.map((card) => ({
		color: card.color,
		count: cardMap[card.color] || card.count,
	}));
};

const OpponentStatus = ({ name, cards_count, tokens, reserved_cards_count, points }) => {
	const completeTokens = addDefaultTokens(tokens);
	const completeCards = addDefaultCards(cards_count);

	return (
		<div className="opponent-status">
			<div className="opponent-header">
				<h3 className="opponent-name">{name}</h3>
				<div className="opponent-points">
					<div className="star-icon">★</div>
					<div className="points-text">{points}</div>
				</div>
			</div>
			<div className="opponent-cards-row">
				{completeCards.map((card) => (
					<div
						key={card.color}
						className={`opponent-card-count ${card.count === 0 ? 'zero' : ''}`}
						style={{ background: colors[card.color] }}
					>
						{card.count}
					</div>
				))}
				<div
					key="gold"
					className={`opponent-card-count ${reserved_cards_count === 0 ? 'zero' : ''}`}
					style={{ background: colors.gold }}
				>
					{reserved_cards_count}
				</div>
			</div>
			<div className="opponent-tokens-row">
				{completeTokens.map((token, index) => (
					<div
						key={index}
						className={`opponent-token-count ${token.count === 0 ? 'zero' : ''}`}
						style={{ background: colors[token.color] }}
					>
						{token.count}
					</div>
				))}
			</div>
		</div>
	);
};

OpponentStatus.propTypes = {
	name: PropTypes.string.isRequired,
	cards_count: PropTypes.arrayOf(
		PropTypes.shape({
			color: PropTypes.string.isRequired,
			count: PropTypes.number.isRequired,
		})
	).isRequired,
	tokens: PropTypes.arrayOf(
		PropTypes.shape({
			color: PropTypes.string.isRequired,
			count: PropTypes.number.isRequired,
		})
	).isRequired,
	reserved_cards_count: PropTypes.number.isRequired,
	points: PropTypes.number.isRequired,
};

export default OpponentStatus;
