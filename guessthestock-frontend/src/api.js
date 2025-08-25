
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export async function fetchTodayGames() {
  const response = await fetch(`${API_URL}/game/today`);

  if (!response.ok) {
    throw new Error('Failed to fetch games');
  }
  

  return response.json();
}