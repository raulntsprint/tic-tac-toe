import { useState, useEffect } from 'react'
import './App.css'
import Board from './components/Board'
import GameControls from './components/GameControls'
import { createNewGame, makeMove, getGameState } from './api/gameApi'

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [gameState, setGameState] = useState(null)
  const [selectedMode, setSelectedMode] = useState('algorithmic')
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')

  const startNewGame = async (mode) => {
    setIsLoading(true)
    setMessage('')
    try {
      const response = await createNewGame(mode)
      setSessionId(response.session_id)
      setGameState(response.state)
      setSelectedMode(mode)
      setMessage(response.message || 'New game started!')
    } catch (error) {
      setMessage('Error creating game: ' + error.message)
      console.error('Error creating game:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleCellClick = async (row, col) => {
    if (!sessionId || !gameState || gameState.game_over || isLoading) {
      return
    }

    if (gameState.board[row][col] !== '') {
      setMessage('Cell already occupied!')
      return
    }

    if (gameState.current_turn !== 'X') {
      setMessage("It's not your turn!")
      return
    }

    setIsLoading(true)
    setMessage('')

    try {
      const response = await makeMove(sessionId, row, col)
      setGameState(response.state)
      
      if (response.message) {
        setMessage(response.message)
      }
    } catch (error) {
      setMessage('Error making move: ' + error.message)
      console.error('Error making move:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    // Start a new game automatically on mount
    startNewGame('algorithmic')
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎮 Tic Tac Toe</h1>
        <p className="subtitle">SSE Code Screen - Advanced AI Challenge.</p>
      </header>

      <main className="app-main">
        <GameControls
          selectedMode={selectedMode}
          onModeChange={setSelectedMode}
          onNewGame={startNewGame}
          isLoading={isLoading}
        />

        {message && (
          <div className={`message ${gameState?.game_over ? 'game-over' : ''}`}>
            {message}
          </div>
        )}

        {gameState && (
          <div className="game-info">
            <p className="turn-indicator">
              {gameState.game_over ? (
                gameState.winner ? (
                  <span className={`winner-${gameState.winner.toLowerCase()}`}>
                    🏆 {gameState.winner} Wins!
                  </span>
                ) : (
                  <span className="draw">🤝 It's a Draw!</span>
                )
              ) : (
                <>
                  Current Turn: 
                  <span className={`player-${gameState.current_turn.toLowerCase()}`}>
                    {' '}{gameState.current_turn}
                  </span>
                </>
              )}
            </p>
            <p className="mode-info">
              Mode: {selectedMode === 'algorithmic' ? '🤖 Minimax Algorithm' : '🧠 Grok AI'}
            </p>
          </div>
        )}

        {gameState && (
          <Board
            board={gameState.board}
            onCellClick={handleCellClick}
            isDisabled={gameState.game_over || isLoading}
            winner={gameState.winner}
          />
        )}

        {isLoading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Thinking...</p>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Built with React, FastAPI, and Docker</p>
        <p className="author">Tic Tac Toe SSE Code Screen</p>
      </footer>
    </div>
  )
}

export default App

