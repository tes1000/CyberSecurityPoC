const express = require('express');
const path = require('path');
const app = express();
const port = 8080;

// Create views directory for our templates
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Custom middleware to prevent path traversal attacks
app.use((req, res, next) => {
  const urlPath = decodeURIComponent(req.path);
  
  // Check for path traversal patterns
  const hasTraversal = urlPath.includes('../') || 
                       urlPath.includes('..\\') || 
                       urlPath.includes('/../') || 
                       urlPath.includes('/..\\');
                       
  // Check for encoded variants
  const hasEncodedTraversal = urlPath.includes('%2e%2e%2f') || 
                              urlPath.includes('%2e%2e/') ||
                              urlPath.includes('..%2f') || 
                              urlPath.includes('%252e%252e%252f');
  
  if (hasTraversal || hasEncodedTraversal) {
    console.log(`Path traversal attempt blocked: ${urlPath}`);
    return res.status(403).send('Access denied: Path traversal attempt detected');
  }
  
  next();
});

// Serve static files, but NOT the root index.html
app.use(express.static(path.join(__dirname), {
  index: false,  // This prevents serving index.html automatically
  dotfiles: 'deny' // Prevent access to dotfiles like .env, .git, etc.
}));

// Main route that renders the template with the parameters
app.get('/', (req, res) => {
  const queryParams = req.query;
  const paramEntries = [];
  
  // Process query parameters
  if (Object.keys(queryParams).length > 0) {
    // Limit number of parameters to prevent abuse
    const limitedParams = Object.entries(queryParams).slice(0, 20);
    
    for (const [key, rawValue] of limitedParams) {
      // Basic validation for extremely large inputs
      if (key.length > 100 || (rawValue && rawValue.length > 5000)) {
        paramEntries.push({
          key: key.substring(0, 100),
          error: "Parameter too long"
        });
        continue;
      }
      
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