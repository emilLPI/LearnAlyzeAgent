const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 5173;
const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8000';
const root = path.join(__dirname, '..', 'app', 'static');

const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml'
};

const API_PREFIXES = [
  '/health',
  '/emails',
  '/tasks',
  '/jobs',
  '/approvals',
  '/audit',
  '/capabilities',
  '/settings',
  '/agent'
];

function isApiPath(urlPath) {
  return API_PREFIXES.some((prefix) => urlPath === prefix || urlPath.startsWith(`${prefix}/`) || urlPath.startsWith(`${prefix}?`));
}

function proxyToBackend(req, res) {
  const target = new URL(req.url, BACKEND_URL);
  const client = target.protocol === 'https:' ? https : http;
  const upstreamReq = client.request(
    {
      protocol: target.protocol,
      hostname: target.hostname,
      port: target.port,
      path: `${target.pathname}${target.search}`,
      method: req.method,
      headers: {
        ...req.headers,
        host: target.host,
      },
    },
    (upstreamRes) => {
      res.statusCode = upstreamRes.statusCode || 502;
      Object.entries(upstreamRes.headers).forEach(([key, value]) => {
        if (typeof value !== 'undefined') res.setHeader(key, value);
      });
      upstreamRes.pipe(res);
    }
  );

  upstreamReq.on('error', () => {
    res.statusCode = 502;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.end(
      JSON.stringify({
        error: 'Backend unavailable',
        hint: `Start FastAPI backend on ${BACKEND_URL} (example: cd agent_control_plane && python -m uvicorn app.main:app --reload)`,
      })
    );
  });

  req.pipe(upstreamReq);
}

http.createServer((req, res) => {
  if (isApiPath(req.url)) {
    return proxyToBackend(req, res);
  }

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
  console.log(`API proxy target: ${BACKEND_URL}`);
  console.log('Server is running. Keep this terminal open, then open the URL above in your browser.');
  console.log('Use HTTP (http://...), not HTTPS. If you open https://localhost you may get ERR_SSL_PROTOCOL_ERROR.');
});
