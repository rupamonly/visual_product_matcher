import React, { useState } from 'react';
import './ImageUploader.css';

function ImageUploader({ onSearch }) {
  // State to hold the selected file
  const [selectedFile, setSelectedFile] = useState(null);

  // Handler for when a file is selected
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Handler for the form submission
  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent the form from reloading the page
    if (selectedFile) {
      console.log('Submitting file:', selectedFile);
      onSearch(selectedFile); // Pass the file to the parent component (App.jsx)
    } else {
      alert('Please select an image file first.');
    }
  };

  return (
    <div className="uploader-container">
      <p>Upload an image of a product to find visually similar items.</p>
      <form onSubmit={handleSubmit} className="uploader-form">
        <input 
          type="file" 
          onChange={handleFileChange} 
          accept="image/png, image/jpeg, image/jpg" 
        />
        <button type="submit">Find Similar</button>
      </form>
    </div>
  );
}

export default ImageUploader;