const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 5173;
const root = path.join(__dirname, '..', 'app', 'static');

const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml'
};

http.createServer((req, res) => {
  let reqPath = req.url === '/' ? '/index.html' : req.url;
  if (reqPath.startsWith('/static/')) reqPath = reqPath.replace('/static', '');
  const filePath = path.normalize(path.join(root, reqPath));

  if (!filePath.startsWith(root)) {
    res.statusCode = 403;
    return res.end('Forbidden');
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.statusCode = 404;
      return res.end('Not Found');
    }
    res.setHeader('Content-Type', mime[path.extname(filePath)] || 'text/plain; charset=utf-8');
    res.end(data);
  });
}).listen(PORT, () => {
  console.log(`ARX UI available at http://localhost:${PORT}`);
});
