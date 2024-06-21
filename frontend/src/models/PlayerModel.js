// models/PlayerModel.js
import CardModel from './CardModel';

export default class PlayerModel {
	constructor(
		id,
		name,
		tokens = { violet: 0, blue: 0, green: 0, red: 0, black: 0, gold: 0 },
		cards = { violet: 0, blue: 0, green: 0, red: 0, black: 0 },
		reservedCards = [],
		points
	) {
		this.id = id;
		this.name = name;
		this.tokens = tokens; // Lista di gettoni
		this.cards = cards;   // Quantità di carte
		this.reservedCards = reservedCards; // Lista di carte riservate
		this.points = points;
	}
}
