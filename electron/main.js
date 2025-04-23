const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
let apiProcess;

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: { preload: path.join(__dirname, "preload.js") },
  });
  win.loadURL("http://localhost:8000");
}

app.whenReady().then(() => {
  apiProcess = spawn("python", ["../backend/app.py"]);
  apiProcess.stdout.on("data", console.log);
  createWindow();
});

app.on("window-all-closed", () => {
  apiProcess.kill();
  app.quit();
});
