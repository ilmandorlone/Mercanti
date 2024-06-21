// src/models/PassengerModel.js
export default class PassengerModel {
	constructor(id, cost = [], points = 0) {
		this.id = id;
		this.cost = cost; // Lista di costi per il viaggiatore
		this.points = points; // Punti vittoria del viaggiatore
	}
}
