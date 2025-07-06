
import React, { useState } from 'react';
import Chart from './Chart';


export default function GameCard({ game, onGuess, hintUsed, setHintUsed,isSolved,date }) {
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
    <div className="bg-card rounded-lg p-4 mb-4 border border-gray-700">
      <h2 className="text-xl font-semibold mb-4">{date}</h2>

      <Chart prices={game.prices} />

    {!isSolved && (
        <>
        <div className='flex flex-wrap items-center columns-3xs gap-2 mt-6'>
            <input 
            className="flex-1 max-w-xs block my-2 p-2 rounded bg-background border border-gray-600 text-text w-32"
            placeholder="Ticker (e.g., AAPL)"
            value={tickerGuess}
            onChange={(e) => setTickerGuess(e.target.value)}
            />

            <input
            className="flex-1 max-w-xs block my-2 p-2 rounded bg-background border border-gray-600 text-text w-32"
            placeholder="Year (optional)"
            value={yearGuess}
            onChange={(e) => setYearGuess(e.target.value)}
            />

            <button className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded disabled:bg-gray-600" 
                onClick={handleHint}>Request Hint</button>

            
            
            <button className="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded"
                onClick={handleSubmit}>Submit Guess
            </button>

        </div>
            <div className="mt-4 flex gap-2">
            {hintUsed && <div className="mt-2 p-2 bg-yellow-100 text-yellow-800 rounded w-fit">
                <p>Industry Hint: {game.industry}</p>    
            </div>}
            </div>
            
        </>
     
    )}
    {isSolved &&(
        <div className="mt-2 bg-green-900 text-green-200 p-2 rounded"><h3>Answer: {game.ticker}, {game.name}</h3></div>
    )}

      {result && (
        <div className={`mt-4 font-bold ${result.correct ? 'text-green-400' : 'text-red-400'}`}>
          {result.correct ? (
            <>
                <p>✅ Correct! You earned {result.points} point(s).</p>
                <div className="mt-1 bg-green-900 text-green-200 p-2 rounded">
                    Solution: {game.ticker}, ({game.end_year.slice(1,-1)})
                </div>
            </>
            
          ) : (
            <p>❌ Incorrect. Lives left: {result.livesLeft}</p>
          )}
        </div>
      )}

    {isSolved && !result?.correct && (
        <div className="mt-4 bg-green-900 text-green-200 p-2 rounded">
          Solution: {game.ticker} ({game.end_year})
        </div>
    )}
    </div>
  );
}