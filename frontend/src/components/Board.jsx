import Cell from './Cell'
import './Board.css'

function Board({ board, onCellClick, isDisabled, winner }) {
  return (
    <div className="board">
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="board-row">
          {row.map((cell, colIndex) => (
            <Cell
              key={`${rowIndex}-${colIndex}`}
              value={cell}
              onClick={() => onCellClick(rowIndex, colIndex)}
              isDisabled={isDisabled}
              isWinningCell={false}
            />
          ))}
        </div>
      ))}
    </div>
  )
}

export default Board

