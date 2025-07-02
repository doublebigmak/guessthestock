import React, { useEffect, useState } from 'react';
import { fetchTodayGames } from './api';
import GameCard from './components/GameCard';
import { getStored, setStored } from './utils';


function App() {
  const todayDateString = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  // Check lastPlayedDate
  const lastPlayedDate = getStored('lastPlayedDate', todayDateString);

  const isSameDay = lastPlayedDate === todayDateString;

  // If same day, use stored; else reset to default

  const [score, setScore] = useState(() => getStored('score', 0));
  const [streak, setStreak] = useState(() => getStored('streak', 0));
  const [lives, setLives] = useState(() => isSameDay ? getStored('lives', 3) : 3);
  const [hintUsed, setHintUsed] = useState(() => isSameDay ? getStored('hintUsed', false) : false);

  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetchTodayGames()
      .then(data => {
        setGames(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    setStored('score', score);
    setStored('streak', streak);
    setStored('lives', lives);
    setStored('hintUsed', hintUsed);
    setStored('lastPlayedDate', todayDateString);

  }, [score, streak, lives, hintUsed,todayDateString]);


  const handleGuess = (game, tickerGuess, yearGuess) => {
    let correct = false;
    let pointsEarned = 0;

    const tickerCorrect = tickerGuess.toUpperCase() === game.ticker.toUpperCase();
    const yearCorrect = parseInt(yearGuess) === game.end_year;

    if (tickerCorrect) {
      correct = true;

      const base = hintUsed ? 1 : 2;
      const bonus = streak;
      pointsEarned = base + bonus + (yearCorrect ? 1 : 0);

      setScore(score + pointsEarned);
      setStreak(streak + 1);
    } else {
      setLives(lives - 1);
      setStreak(0);
    }

    return {
      correct,
      points: pointsEarned,
      livesLeft: lives - (correct ? 0 : 1),
    };
  };



  return (
    <div>
      <h1>Guess The Stock 📈</h1>
      <p>🏆 Score: {score} | 🔥 Streak: {streak} | ❤️ Lives: {lives}</p>

      {loading && <p>Loading games...</p>}
      {!loading && games.length === 0 && <p>No games found.</p>}
      {!loading && games.map(game => (
        <GameCard
          key={game.id}
          game={game}
          onGuess={handleGuess}
          hintUsed={hintUsed}
          setHintUsed={setHintUsed}
        />
      ))}
    </div>
  );
}


export default App;
