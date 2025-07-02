
import React, { useState } from 'react';
import Chart from './Chart';


export default function GameCard({ game, onGuess, hintUsed, setHintUsed }) {
    //game object, Guess action, 
  const [tickerGuess, setTickerGuess] = useState('');
  const [yearGuess, setYearGuess] = useState('');
  const [result, setResult] = useState(null);

  const handleHint = () => {
    if (!hintUsed) {
      setHintUsed(true);
    } else {
      alert("You already used your hint today!");
    }
  };

  const handleSubmit = () => {
    // Pass to parent
    const outcome = onGuess(game, tickerGuess.trim(), yearGuess.trim());
    setResult(outcome);
  };

  return (
    <div className="game-card">
      <h2>Guess the Stock!</h2>

      <Chart prices={game.prices} />

      <div style={{ marginTop: '1em' }}>
        <input
          placeholder="Guess ticker (e.g., AAPL)"
          value={tickerGuess}
          onChange={(e) => setTickerGuess(e.target.value)}
        />

        <input
          placeholder="Guess end year (optional)"
          value={yearGuess}
          onChange={(e) => setYearGuess(e.target.value)}
        />
      </div>

      <button onClick={handleHint}>Request Hint</button>
      {hintUsed && <p>Industry Hint: {game.industry}</p>}
      <button onClick={handleSubmit}>Submit Guess</button>

      {result && (
        <div style={{ marginTop: '1em' }}>
          {result.correct ? (
            <p>✅ Correct! You earned {result.points} points.</p>
          ) : (
            <p>❌ Incorrect. Lives left: {result.livesLeft}</p>
          )}
        </div>
      )}
    </div>
  );
}