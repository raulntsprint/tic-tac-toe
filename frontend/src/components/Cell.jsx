import './Cell.css'

function Cell({ value, onClick, isDisabled }) {
  const cellClass = `cell ${value ? `cell-${value.toLowerCase()}` : ''} ${isDisabled ? 'disabled' : ''}`

  return (
    <button
      className={cellClass}
      onClick={onClick}
      disabled={isDisabled || value !== ''}
      aria-label={value || 'empty cell'}
    >
      {value}
    </button>
  )
}

export default Cell

