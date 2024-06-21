// utils/canAffordCard.js
export const canAffordCard = (player, card) => {
	if (!player || !player.tokens || !player.cards_count || !card || !card.cost) return false;

	// Costruisci il tokenCounter dalle proprietà del giocatore
	const tokenCounter = player.tokens.reduce((acc, token) => {
		acc[token.color] = token.count;
		return acc;
	}, {});

	// Costruisci il discountCounter dalle carte del giocatore
	const discountCounter = player.cards_count.reduce((acc, card) => {
		acc[card.color] = (acc[card.color] || 0) + card.count;
		return acc;
	}, {});

	let missingTokens = 0;

	for (const [color, cost] of Object.entries(card.cost)) {
		const effectiveCost = Math.max(0, cost - (discountCounter[color] || 0)); // Apply discount
		const tokensInPossession = tokenCounter[color] || 0;

		if (tokensInPossession < effectiveCost) {
			missingTokens += effectiveCost - tokensInPossession;
		}
	}

	return missingTokens <= (tokenCounter['gold'] || 0);
};
