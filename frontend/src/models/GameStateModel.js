// src/models/GameStateModel.js

import PassengerModel from './PassengerModel';

export default class GameStateModel {
	constructor(
		opponents = [],
		player = null,
		remaining_cards = { level1: 0, level2: 0, level3: 0 },
		tokens = [
			{ color: 'violet', count: 0 },
			{ color: 'blue', count: 0 },
			{ color: 'green', count: 0 },
			{ color: 'red', count: 0 },
			{ color: 'black', count: 0 },
			{ color: 'gold', count: 0 }
		],
		visible_level1 = [],
		visible_level2 = [],
		visible_level3 = [],
		tempTokens = { violet: 0, blue: 0, green: 0, red: 0, black: 0, gold: 0 },
		visible_passengers = []
	) {
		this.opponents = opponents;
		this.player = player;
		this.remaining_cards = remaining_cards;
		this.tokens = tokens;
		this.visible_level1 = visible_level1;
		this.visible_level2 = visible_level2;
		this.visible_level3 = visible_level3;
		this.tempTokens = tempTokens;
		this.visible_passengers = visible_passengers.map(passenger => new PassengerModel(passenger.id, passenger.cost, passenger.points));
	}
}
