const express = require('express');
const path = require('path');
const app = express();
const port = 8080;

// Create views directory for our templates
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files, but NOT the root index.html
app.use(express.static(path.join(__dirname), {
  index: false  // This prevents serving index.html automatically
}));

// Main route that renders the template with the parameters
app.get('/', (req, res) => {
  const queryParams = req.query;
  const paramEntries = [];
  
  // Process query parameters
  if (Object.keys(queryParams).length > 0) {
    for (const [key, rawValue] of Object.entries(queryParams)) {
      try {
        const decodedOnce = decodeURIComponent(rawValue);
        const decodedTwice = decodeURIComponent(decodedOnce);
        
        // Check if the parameter contains potentially malicious code
        const isVulnerable = /<\s*script|on\w+\s*=|<\s*img[^>]*onerror\s*=|javascript:/i.test(decodedTwice);
        
        paramEntries.push({
          key,
          rawValue, 
          decodedOnce,
          decodedTwice,
          isVulnerable
        });
      } catch (e) {
        paramEntries.push({
          key,
          error: e.message
        });
      }
    }
  }

  // Render the template with the processed parameters
  res.render('index', {
    paramEntries,
    hasParams: paramEntries.length > 0
  });
});

app.listen(port, () => {
  console.log(`Reflected XSS demo server running at http://localhost:${port}`);
});