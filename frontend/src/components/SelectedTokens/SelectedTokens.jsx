// src/components/SelectedTokens/SelectedTokens.jsx
import React from 'react';
import PropTypes from 'prop-types';
import './SelectedTokens.css';
import colors from '../../utils/colors';

const SelectedTokens = ({ selectedTokens = {}, onRemoveToken }) => {
	console.log('SelectedTokens render, selectedTokens:', selectedTokens); // Log

	const tokensArray = Object.entries(selectedTokens).reduce((acc, [color, count]) => {
		for (let i = 0; i < count; i++) {
			acc.push(color);
		}
		return acc;
	}, []);

	return (
		<div className="selected-tokens">
			{selectedTokens.map((color) => (
				<div
					className="token"
					style={{ background: colors[color] }}
					onClick={() => onRemoveToken(color)}
				/>
			))}
		</div>
	);
};

SelectedTokens.propTypes = {
	selectedTokens: PropTypes.objectOf(PropTypes.number),
	onRemoveToken: PropTypes.func.isRequired,
};

export default SelectedTokens;
