import React from 'react';
import PropTypes from 'prop-types';
import colors from '../../utils/colors';
import './PassengerCard.css';

const PassengerCard = ({ id, cost, points }) => {
	return (
		<div className="passenger-card">
			<div className="passenger-cost">
				{cost.filter(({ count }) => count > 0).map(({ color, count }) => (
					<div key={color} className="passenger-cost-item" style={{ background: colors[color] }}>
						{count}
					</div>
				))}
			</div>
			<div className="passenger-points">
				<span className="points">{points}</span>
			</div>
		</div>
	);
};

PassengerCard.propTypes = {
	id: PropTypes.number.isRequired,
	cost: PropTypes.arrayOf(
		PropTypes.shape({
			color: PropTypes.string.isRequired,
			count: PropTypes.number.isRequired,
		})
	).isRequired,
	points: PropTypes.number.isRequired,
};

export default PassengerCard;
