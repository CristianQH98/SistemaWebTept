const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let backendProcess;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true
    }
  });

  win.loadFile(path.join(__dirname, 'frontend', 'index.html'));
}

// Iniciar app Python al abrir Electron
app.whenReady().then(() => {
  // Ejecutar el backend
  backendProcess = spawn('python', ['backend/app.py'], {
    cwd: __dirname,
    shell: true
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`🟢 Backend: ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
  console.log(`📢 Backend log: ${data}`);
});


  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Detener backend al cerrar Electron
app.on('window-all-closed', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
  if (process.platform !== 'darwin') app.quit();
});
