const { spawn } = require('child_process');
const path = require('path');

const root = path.join(__dirname, '..');
const pythonCmd = process.env.PYTHON_CMD || (process.platform === 'win32' ? 'python' : 'python3');
const backendHost = process.env.BACKEND_HOST || '127.0.0.1';
const backendPort = process.env.BACKEND_PORT || '8000';
const uiPort = process.env.PORT || '5173';

function spawnProcess(command, args, name, cwd = root) {
  const child = spawn(command, args, {
    cwd,
    stdio: 'inherit',
    shell: process.platform === 'win32',
  });

  child.on('exit', (code) => {
    if (code !== 0) {
      console.error(`[${name}] exited with code ${code}`);
    }
  });

  return child;
}

console.log(`Starting ARX full stack...`);
console.log(`- UI: http://localhost:${uiPort}`);
console.log(`- API: http://${backendHost}:${backendPort}`);
console.log(`- Python command: ${pythonCmd}`);

const backend = spawnProcess(
  pythonCmd,
  ['-m', 'uvicorn', 'app.main:app', '--host', backendHost, '--port', backendPort, '--reload'],
  'backend',
  root
);
const ui = spawnProcess('node', ['scripts/serve-static.js'], 'ui', root);

function shutdown() {
  if (!backend.killed) backend.kill('SIGTERM');
  if (!ui.killed) ui.kill('SIGTERM');
}

process.on('SIGINT', () => {
  shutdown();
  process.exit(0);
});
process.on('SIGTERM', () => {
  shutdown();
  process.exit(0);
});
