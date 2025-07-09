import React, { useState } from 'react';

function Square({ value, onClick }) {
  return (
    <button 
      onClick={onClick} 
      style={{
        width: '60px',
        height: '60px',
        fontSize: '24px',
        fontWeight: 'bold',
      }}
    >
      {value}
    </button>
  );
}

function Board({ squares, onSquareClick }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 60px)', gap: '5px' }}>
      {squares.map((val, i) => (
        <Square key={i} value={val} onClick={() => onSquareClick(i)} />
      ))}
    </div>
  );
}

function App() {
  const [history, setHistory] = useState([Array(9).fill(null)]);
  const [currentStep, setCurrentStep] = useState(0);
  const [xIsNext, setXIsNext] = useState(true);

  const currentSquares = history[currentStep];

  function calculateWinner(squares) {
    const lines = [
      [0,1,2], [3,4,5], [6,7,8], // rows
      [0,3,6], [1,4,7], [2,5,8], // columns
      [0,4,8], [2,4,6]           // diagonals
    ];
    for (let [a,b,c] of lines) {
      if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
        return squares[a];
      }
    }
    return null;
  }

  const winner = calculateWinner(currentSquares);
  const status = winner 
    ? `Winner: ${winner}` 
    : `Next player: ${xIsNext ? 'X' : 'O'}`;

  function handleClick(i) {
    const past = history.slice(0, currentStep + 1);
    const current = past[past.length - 1];
    const squares = current.slice();

    if (calculateWinner(squares) || squares[i]) return;

    squares[i] = xIsNext ? 'X' : 'O';
    setHistory([...past, squares]);
    setCurrentStep(past.length);
    setXIsNext(!xIsNext);
  }

  function jumpTo(step) {
    setCurrentStep(step);
    setXIsNext(step % 2 === 0);
  }

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '40px',
        fontFamily: 'Arial, sans-serif',
        marginTop: '40px',
      }}
    >
      {/* Left side: Game Board */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <h1>Tic Tac Toe</h1>
        <Board squares={currentSquares} onSquareClick={handleClick} />
        <p style={{ marginTop: '20px', fontSize: '18px' }}>{status}</p>
        <button
          onClick={() => {
            setHistory([Array(9).fill(null)]);
            setCurrentStep(0);
            setXIsNext(true);
          }}
          style={{
            marginTop: '10px',
            padding: '8px 16px',
            fontSize: '16px',
            cursor: 'pointer',
          }}
        >
          Restart Game
        </button>
      </div>

      {/* Right side: Step history */}
      <div>
        <h3>Steps</h3>
        <ol style={{ paddingLeft: '20px' }}>
          {history.map((_, move) => {
            const desc = move === 0 ? 'Go to game start' : `Go to step #${move} (${move % 2 === 0 ? 'O' : 'X'})`;
            return (
              <li key={move}>
                <button
                  onClick={() => jumpTo(move)}
                  style={{
                    marginBottom: '5px',
                    padding: '5px 10px',
                    cursor: 'pointer',
                    backgroundColor: move === currentStep ? '#d3d3d3' : 'grey',
                    color: 'black',
                  }}
                >
                  {desc}
                </button>
              </li>
            );
          })}
        </ol>
      </div>
    </div>
  );
}

export default App;
