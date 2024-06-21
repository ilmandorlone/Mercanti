// utils/canReserveCard.js
export const canReserveCard = (player) => {
	if (!player || !player.reserved_cards) return false;
	return player.reserved_cards.length < 3;
};
