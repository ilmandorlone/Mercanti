// src/components/PlayerStatus/PlayerStatus.jsx
import React from 'react';
import PropTypes from 'prop-types';
import './PlayerStatus.css';
import colors from '../../utils/colors';
import Card from '../Card/Card';

const defaultCards = [
	{ color: 'violet', count: 0 },
	{ color: 'blue', count: 0 },
	{ color: 'green', count: 0 },
	{ color: 'red', count: 0 },
	{ color: 'black', count: 0 },
];

const defaultTokens = [
	{ color: 'violet', count: 0 },
	{ color: 'blue', count: 0 },
	{ color: 'green', count: 0 },
	{ color: 'red', count: 0 },
	{ color: 'black', count: 0 },
	{ color: 'gold', count: 0 },
];

const addDefaultCards = (cards = []) => {
	const cardMap = cards.reduce((acc, card) => {
		acc[card.color] = card.count;
		return acc;
	}, {});

	return defaultCards.map((card) => ({
		color: card.color,
		count: cardMap[card.color] || card.count,
	}));
};

const addDefaultTokens = (tokens = []) => {
	const tokenMap = tokens.reduce((acc, token) => {
		acc[token.color] = token.count;
		return acc;
	}, {});

	return defaultTokens.map((token) => ({
		color: token.color,
		count: tokenMap[token.color] || token.count,
	}));
};

const PlayerStatus = ({ cards_count, tokens, reservedCards, player }) => {
	const completeCards = addDefaultCards(cards_count);
	const completeTokens = addDefaultTokens(tokens);

	return (
		<div className="player-status">
			<div className="cards-tokens-wrapper">
				<div className="cards">
					{completeCards.map((card, index) => (
						<div
							key={index}
							className={`card-rect ${card.count === 0 ? 'zero' : ''}`}
							style={{ background: colors[card.color] }}
						>
							<span className="card-count">{card.count}</span>
						</div>
					))}
					<div
						className={`card-rect reserved`}
						style={{ background: 'transparent', border: '0px' }}
					>
					</div>
				</div>
				<div className="tokens_player">
					{completeTokens.map((token, index) => (
						<div
							key={index}
							className={`player-status-token ${token.count === 0 ? 'zero' : ''}`}
							style={{ background: colors[token.color] }}
						>
							<span>{token.count}</span>
						</div>
					))}
				</div>
			</div>
			<div className="reserved-cards">
				{reservedCards.map((card, index) => (
					<Card
						key={index}
						cardId={card.id}
						colorName={card.color}
						cost={card.cost.reduce((acc, { color, count }) => {
							acc[color] = count;
							return acc;
						}, {})}
						player={player}
						level="reserved"
						className="reserved"
					/>
				))}
			</div>
		</div>
	);
};

PlayerStatus.propTypes = {
	cards_count: PropTypes.arrayOf(
		PropTypes.shape({
			color: PropTypes.string.isRequired,
			count: PropTypes.number.isRequired,
		})
	),
	tokens: PropTypes.arrayOf(
		PropTypes.shape({
			color: PropTypes.string.isRequired,
			count: PropTypes.number.isRequired,
		})
	),
	reservedCards: PropTypes.array.isRequired,
	player: PropTypes.object.isRequired,
};

export default PlayerStatus;
