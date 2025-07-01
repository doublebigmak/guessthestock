import React, { useEffect, useState } from 'react';
import { fetchTodayGames } from './api';
import GameCard from './components/GameCard';

function App() {
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

  return (
    <div>
      <h1>Guess The Stock 📈</h1>
      {loading && <p>Loading games...</p>}
      {!loading && games.length === 0 && <p>No games found.</p>}
      {!loading && games.map(game => (
        <GameCard key={game.id} game={game} />
      ))}
    </div>
  );
}

export default App;
