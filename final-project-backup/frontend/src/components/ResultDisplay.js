import React from 'react';

function ResultDisplay({ result }) {
  return (
    <div>
      <h2>Result</h2>
      <div style={{ whiteSpace: 'pre-wrap', border: '1px solid #ccc', padding: '10px' }}>
        {result}
      </div>
    </div>
  );
}

export default ResultDisplay;
