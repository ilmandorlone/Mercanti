// models/CardModel.js
export default class CardModel {
	constructor(id, level, colorName, cost = { violet: 0, blue: 0, green: 0, red: 0, black: 0 }, points = 0) {
		this.id = id;
		this.level = level;
		this.colorName = colorName;
		this.cost = cost; // Costo della carta in termini di gettoni colorati
		this.points = points; // Punti vittoria della carta
	}
}
