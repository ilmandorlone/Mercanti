import React from 'react';
import PlayerStatus from '../PlayerStatus/PlayerStatus';
import OpponentStatus from '../OpponentStatus/OpponentStatus';
import TokenList from '../TokenList/TokenList';
import SelectedTokens from '../SelectedTokens/SelectedTokens';
import { useGameContext } from '../../context/GameContext';
import './GridLayout.css';
import CardModel from '../../models/CardModel';
import CardRow from '../CardRow/CardRow';
import PassengerList from '../PassengerList/PassengerList'; // Importa il nuovo componente PassengerList

const GridLayout = () => {
	const { gameState, addToken, removeToken, selectedTokens, endTurn } = useGameContext();

	const currentPlayer = gameState?.player || {};
	const reservedCards = currentPlayer?.reserved_cards || [];

	const opponents = gameState?.opponents?.map(opponent => ({
		id: opponent.id,
		name: opponent.name,
		cards_count: opponent.cards_count,
		tokens: opponent.tokens,
		reserved_cards_count: opponent.reserved_cards_count,
		points: opponent.points,
	})) || [];

	const cardsLevel1 = (gameState?.visible_level1 || []).map(card => new CardModel(card.id, card.level, card.color, card.cost, card.points));
	const cardsLevel2 = (gameState?.visible_level2 || []).map(card => new CardModel(card.id, card.level, card.color, card.cost, card.points));
	const cardsLevel3 = (gameState?.visible_level3 || []).map(card => new CardModel(card.id, card.level, card.color, card.cost, card.points));
	const visiblePassengers = gameState?.visible_passengers || []; // Aggiungi le tessere viaggiatore visibili

	return (
		<div className="container">
			<div className="top-section">
				<div className="players-area">
					{opponents.map((opponent, index) => (
						<OpponentStatus
							key={index}
							name={opponent.name}
							cards_count={opponent.cards_count}
							tokens={opponent.tokens}
							reserved_cards_count={opponent.reserved_cards_count}
							points={opponent.points}
						/>
					))}
				</div>
				<GameBoard
					cardsLevel1={cardsLevel1}
					cardsLevel2={cardsLevel2}
					cardsLevel3={cardsLevel3}
					remainingCards={gameState?.remaining_cards}
					currentPlayer={currentPlayer}
				/>
				<div className="tokens-area">
					<TokenList tokens={gameState?.tokens} onSelectToken={addToken} />
				</div>
				<div className="passengers-area">
					<PassengerList passengers={visiblePassengers} />
				</div>
			</div>
			<div className="bottom-section">
				<div className="player-status-wrapper">
					<PlayerStatus
						cards_count={currentPlayer?.cards_count}
						tokens={currentPlayer?.tokens}
						reservedCards={reservedCards}
						player={currentPlayer}
					/>
				</div>
				<div className="selected-tokens-wrapper">
					<SelectedTokens selectedTokens={selectedTokens} onRemoveToken={removeToken} />
					<button className="end-turn-button" onClick={endTurn}>END TURN</button>
				</div>
			</div>
		</div>
	);
};

const GameBoard = ({ cardsLevel1, cardsLevel2, cardsLevel3, remainingCards, currentPlayer }) => {
	return (
		<div className="board-area">
			<CardRow level={3} rowIndex={3} cards={cardsLevel3} remainingCards={remainingCards?.level3} player={currentPlayer} />
			<CardRow level={2} rowIndex={2} cards={cardsLevel2} remainingCards={remainingCards?.level2} player={currentPlayer} />
			<CardRow level={1} rowIndex={1} cards={cardsLevel1} remainingCards={remainingCards?.level1} player={currentPlayer} />
		</div>
	);
};

export default GridLayout;
