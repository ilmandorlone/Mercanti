import React from 'react';
import PropTypes from 'prop-types';
import './TokenList.css';
import colors from '../../utils/colors';
import { useGameContext } from '../../context/GameContext';

const TokenList = ({ tokens }) => {
	const { addToken } = useGameContext(); // Usa addToken dal contesto

	return (
		<div className="token-list">
			{tokens.map((token, index) => (
				<div
					key={index}
					className="token"
					style={{ background: colors[token.color] }}
					onClick={() => addToken(token.color)} // Chiama addToken al click
				>
					<span className="token-count">{token.count}</span>
				</div>
			))}
		</div>
	);
};

TokenList.propTypes = {
	tokens: PropTypes.arrayOf(PropTypes.shape({
		color: PropTypes.string.isRequired,
		count: PropTypes.number.isRequired
	})).isRequired,
};

export default TokenList;
