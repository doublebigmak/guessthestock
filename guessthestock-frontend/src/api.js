

export async function fetchTodayGames() {
  const response = await fetch('http://localhost:8000/game/today');

  if (!response.ok) {
    throw new Error('Failed to fetch games');
  }

  return response.json();
}