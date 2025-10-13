import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import ImageUploader from './components/ImageUploader';
import Loader from './components/Loader';
import ResultsGrid from './components/ResultsGrid';

function App() {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = (file) => {
    setIsLoading(true);
    setResults([]);
    setError(null);

    const formData = new FormData();
    formData.append('image', file);

    axios.post('http://127.0.0.1:5000/api/find-similar', formData)
      .then(response => {
        setResults(response.data);
      })
      .catch(err => {
        console.error('API Error:', err);
        setError('Something went wrong. Please try again.');
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  return (
    <div className="App">
      <h1>Visual Product Matcher ✨</h1>
      <ImageUploader onSearch={handleSearch} />

      {isLoading && <Loader />}
      {error && <p className="error-message">{error}</p>}
      {results.length > 0 && <ResultsGrid results={results} />}
    </div>
  );
}

export default App;



