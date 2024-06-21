// src/components/CardButtons/CardButtons.jsx
import React from 'react';
import PropTypes from 'prop-types';
import './CardButtons.css';
import { useWebSocket } from '../../context/WebSocketContext';
import { useCardContext } from '../../context/CardContext';
import { canAffordCard } from '../../utils/canAffordCard';
import { canReserveCard } from '../../utils/canReserveCard';

const CardButtons = ({ cardId, showPurchase, player, card, level }) => {
	const { sendMessage, playerId } = useWebSocket();
	const { selectedCard } = useCardContext();

	const handlePurchaseClick = () => {
		const message = {
			action: 'purchase_card',
			player_id: playerId,
			card_id: cardId,
		};
		sendMessage(message);
	};

	const handleReserveClick = () => {
		const message = {
			action: 'reserve_card',
			player_id: playerId,
			card_id: cardId || null,
			level: level || 1, // Assicurati che level non sia null
		};
		sendMessage(message);
	};

	const affordable = player && card && canAffordCard(player, card);
	const canReserve = player && canReserveCard(player);

	return (
		<div className="buttons">
			{showPurchase && (
				<button
					className={`button purchase ${!affordable ? 'disabled' : ''}`}
					onClick={affordable ? handlePurchaseClick : null}
					disabled={!affordable}
				>
					<span className="icon">&#10003;</span> Purchase
				</button>
			)}
			<button
				className={`button reserve ${!canReserve ? 'disabled' : ''}`}
				onClick={canReserve ? handleReserveClick : null}
				disabled={!canReserve}
			>
				<span className="icon">&#x2193;</span> Reserve
			</button>
		</div>
	);
};

CardButtons.propTypes = {
	cardId: PropTypes.number,
	showPurchase: PropTypes.bool,
	player: PropTypes.object.isRequired,
	card: PropTypes.object,
	level: PropTypes.number.isRequired,
};

CardButtons.defaultProps = {
	showPurchase: true,
};

export default CardButtons;
