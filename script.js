const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('userInput');
const micButton = document.getElementById('micButton');
const statusText = document.getElementById('status-text');
const themeToggle = document.getElementById('themeToggle');

// --- Typing animation ---
function typeMessage(element, text) {
    let i = 0;
    element.textContent = "";
    element.classList.remove('typing');

    function typing() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            chatWindow.scrollTop = chatWindow.scrollHeight;
            setTimeout(typing, 30);
        }
    }
    typing();
}

// --- Eel exposed functions ---
eel.expose(addMessage);
function addMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender.toLowerCase());

    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('bubble');

    messageDiv.appendChild(bubbleDiv);
    chatWindow.appendChild(messageDiv);

    if (sender.toLowerCase() === 'assistant') {
        bubbleDiv.classList.add('typing');
        statusText.textContent = "ALEX IS TYPING...";
        setTimeout(() => {
            typeMessage(bubbleDiv, message);
            statusText.textContent = "SYSTEM ONLINE";
        }, 500);
    } else {
        bubbleDiv.textContent = message;
    }

    chatWindow.scrollTop = chatWindow.scrollHeight;
}

eel.expose(closeWindow);
function closeWindow() {
    setTimeout(() => { window.close(); }, 2000);
}

// --- Input handling ---
function processUserInput() {
    const command = userInput.value;
    if (command.trim() !== "") {
        addMessage("User", command);
        eel.process_command(command);
        userInput.value = "";
    }
}

userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        processUserInput();
    }
});

// --- Voice recognition ---
micButton.addEventListener('click', () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    addMessage("System", "Listening...");
    micButton.classList.add('listening');
    statusText.textContent = "LISTENING...";

    recognition.start();

    recognition.onresult = (event) => {
        const speechResult = event.results[0][0].transcript;
        addMessage("User", speechResult);
        eel.process_command(speechResult);
    };

    recognition.onspeechend = () => {
        recognition.stop();
        micButton.classList.remove('listening');
        statusText.textContent = "SYSTEM ONLINE";
    };

    recognition.onerror = (event) => {
        addMessage("System", "Error: " + event.error);
        micButton.classList.remove('listening');
        statusText.textContent = "SYSTEM ONLINE";
    };
});

// --- Theme toggle ---
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    themeToggle.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
});
