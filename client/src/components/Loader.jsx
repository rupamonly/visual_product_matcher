import React from 'react';
import './Loader.css';

function Loader() {
  return (
    <div className="loader-container">
      <div className="loader"></div>
      <p>Finding similar products...</p>
    </div>
  );
}

export default Loader;