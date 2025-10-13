import React, { useState } from 'react';
import axios from 'axios'; // Import axios
import './App.css';
import ImageUploader from './components/ImageUploader';

function App() {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // This is the function we will update
  const handleSearch = (file) => {
    setIsLoading(true);
    setResults([]);
    setError(null);

    // Create a FormData object to send the file
    const formData = new FormData();
    // The key 'image' must match what our Flask server expects
    formData.append('image', file);

    // Make the POST request to our backend API
    axios.post('http://127.0.0.1:5000/api/find-similar', formData)
      .then(response => {
        console.log('API Response:', response.data); // Log the results to see them!
        setResults(response.data); // Store the results in our state
      })
      .catch(err => {
        console.error('API Error:', err);
        setError('Something went wrong. Please try again.'); // Set an error message
      })
      .finally(() => {
        setIsLoading(false); // Stop the loading state
      });
  };

  return (
    <div className="App">
      <h1>Visual Product Matcher ✨</h1>
      <ImageUploader onSearch={handleSearch} />

      {/* We will display the results here soon */}
    </div>
  );
}

export default App;