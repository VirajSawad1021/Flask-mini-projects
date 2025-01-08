let timerDuration = 25 * 60; // 25 minutes in seconds
let breakDuration = 5 * 60; // 5 minutes in seconds
let isBreak = false;
let timerInterval;

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function startTimer() {
    let timeLeft = isBreak ? breakDuration : timerDuration;
    document.getElementById('start-button').disabled = true;

    timerInterval = setInterval(() => {
        document.getElementById('timer').textContent = formatTime(timeLeft);
        timeLeft--;

        if (timeLeft < 0) {
            clearInterval(timerInterval);
            isBreak = !isBreak;
            document.getElementById('start-button').disabled = false;
            document.getElementById('timer').textContent = isBreak ? 'Break Time!' : 'Pomodoro Completed!';
        }
    }, 1000);
}

document.getElementById('start-button').addEventListener('click', startTimer);
