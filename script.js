// Local time
function updateClock() {
  const now = new Date();
  document.getElementById("clock").textContent = now.toLocaleTimeString();
}
setInterval(updateClock, 1000);

// Stopwatch
let stopwatchInterval, stopwatchTime = 0;
function startStopwatch() {
  if (!stopwatchInterval) {
    stopwatchInterval = setInterval(() => {
      stopwatchTime++;
      document.getElementById("stopwatch-display").textContent =
        new Date(stopwatchTime * 1000).toISOString().substr(11, 8);
    }, 1000);
  }
}
function pauseStopwatch() { clearInterval(stopwatchInterval); stopwatchInterval = null; }
function resetStopwatch() { pauseStopwatch(); stopwatchTime = 0; document.getElementById("stopwatch-display").textContent = "00:00:00"; }

// Timer
let timerInterval, timerRemaining = 0;
function startTimer() {
  const minutes = parseInt(document.getElementById("minutes").value) || 0;
  const seconds = parseInt(document.getElementById("seconds").value) || 0;
  timerRemaining = minutes * 60 + seconds;
  if (!timerInterval) {
    timerInterval = setInterval(() => {
      if (timerRemaining > 0) {
        timerRemaining--;
        const m = Math.floor(timerRemaining / 60);
        const s = timerRemaining % 60;
        document.getElementById("timer-display").textContent =
          `${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
      } else {
        clearInterval(timerInterval);
        timerInterval = null;
        alert("⏰ Timer finished!");
      }
    }, 1000);
  }
}
function pauseTimer() { clearInterval(timerInterval); timerInterval = null; }
function resetTimer() { pauseTimer(); document.getElementById("timer-display").textContent = "00:00"; }