import React, { useState } from 'react';
import './ImageUploader.css';

function ImageUploader({ onSearch }) {
  
  const [selectedFile, setSelectedFile] = useState(null);

  
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  
  const handleSubmit = (event) => {
    event.preventDefault();
    if (selectedFile) {
      console.log('Submitting file:', selectedFile);
      onSearch(selectedFile);
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