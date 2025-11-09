import axios from 'axios'

// Determine the API base URL based on environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Create a new game session
 * @param {string} mode - Game mode ('algorithmic' or 'grok_ai')
 * @returns {Promise} Response with session_id and initial game state
 */
export const createNewGame = async (mode = 'algorithmic') => {
  try {
    const response = await api.post('/api/game/new', { mode })
    return response.data
  } catch (error) {
    console.error('Error creating new game:', error)
    throw error
  }
}

/**
 * Make a move in the game
 * @param {string} sessionId - Session ID
 * @param {number} row - Row index (0-2)
 * @param {number} col - Column index (0-2)
 * @returns {Promise} Response with updated game state
 */
export const makeMove = async (sessionId, row, col) => {
  try {
    const response = await api.post(`/api/game/${sessionId}/move`, {
      row,
      col,
    })
    return response.data
  } catch (error) {
    console.error('Error making move:', error)
    throw error
  }
}

/**
 * Get the current game state
 * @param {string} sessionId - Session ID
 * @returns {Promise} Response with current game state
 */
export const getGameState = async (sessionId) => {
  try {
    const response = await api.get(`/api/game/${sessionId}/state`)
    return response.data
  } catch (error) {
    console.error('Error getting game state:', error)
    throw error
  }
}

/**
 * Delete a game session
 * @param {string} sessionId - Session ID
 * @returns {Promise} Response confirming deletion
 */
export const deleteGame = async (sessionId) => {
  try {
    const response = await api.delete(`/api/game/${sessionId}`)
    return response.data
  } catch (error) {
    console.error('Error deleting game:', error)
    throw error
  }
}

export default api

