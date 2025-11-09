import './GameControls.css'

function GameControls({ selectedMode, onModeChange, onNewGame, isLoading }) {
  const handleNewGame = () => {
    onNewGame(selectedMode)
  }

  return (
    <div className="game-controls">
      <div className="control-group">
        <label htmlFor="mode-select">AI Mode:</label>
        <select
          id="mode-select"
          value={selectedMode}
          onChange={(e) => onModeChange(e.target.value)}
          disabled={isLoading}
        >
          <option value="algorithmic">🤖 Minimax Algorithm</option>
          <option value="grok_ai">🧠 Grok AI</option>
        </select>
      </div>

      <button
        onClick={handleNewGame}
        disabled={isLoading}
        className="new-game-button"
      >
        {isLoading ? '⏳ Loading...' : '🎮 New Game'}
      </button>
    </div>
  )
}

export default GameControls

