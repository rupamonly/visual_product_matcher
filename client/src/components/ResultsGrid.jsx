import React from 'react';
import './ResultsGrid.css';

function ResultsGrid({ results }) {
  return (
    <div>
      <h2>Top Matches</h2>
      <div className="results-grid">
        {results.map((product) => (
          <div key={product.id} className="product-card">
            <img src={product.image_url} alt={product.name} />
            <div className="product-info">
              <h4 className="product-name">{product.name}</h4>
              <p className="product-category">{product.category}</p>
              <p className="similarity-score">
                Similarity: {Math.round(product.similarity_score * 100)}%
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ResultsGrid;