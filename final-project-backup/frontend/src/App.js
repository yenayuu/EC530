import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import ResultDisplay from './components/ResultDisplay';

function App() {
  const [result, setResult] = useState('');

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Teacher Assistant App</h1>
      <UploadForm setResult={setResult} />
      <ResultDisplay result={result} />
    </div>
  );
}

export default App;
