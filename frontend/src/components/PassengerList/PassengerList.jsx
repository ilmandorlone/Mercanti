import React from 'react';
import PropTypes from 'prop-types';
import PassengerCard from '../PassengerCard/PassengerCard';
import './PassengerList.css';

const PassengerList = ({ passengers }) => {
	return (
		<div className="passenger-list">
			{passengers.map(passenger => (
				<PassengerCard
					key={passenger.id}
					id={passenger.id}
					cost={passenger.cost}
					points={passenger.points}
				/>
			))}
		</div>
	);
};

PassengerList.propTypes = {
	passengers: PropTypes.arrayOf(
		PropTypes.shape({
			id: PropTypes.number.isRequired,
			cost: PropTypes.arrayOf(
				PropTypes.shape({
					color: PropTypes.string.isRequired,
					count: PropTypes.number.isRequired,
				})
			).isRequired,
			points: PropTypes.number.isRequired,
		})
	).isRequired,
};

export default PassengerList;
