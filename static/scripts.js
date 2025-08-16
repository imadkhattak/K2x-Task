async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  // Add user message to chat
  addMessage(message, 'user');
  input.value = "";
  
  try {
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    // Remove typing indicator
    removeTypingIndicator(typingId);

    const data = await response.json();

    if (data.error) {
      addMessage(`Error: ${data.error}`, 'bot', 'error');
    } else {
      // Format SQL and data nicely
      const sqlHtml = `<div class="sql-code">${data.sql}</div>`;
      const dataHtml = formatData(data.data);
      
      addMessage(`
        ${sqlHtml}
        <div class="data-section">
          <h4>Results:</h4>
          ${dataHtml}
        </div>
        <div class="meta-info">
          ${data.from_cache ? '⚡ From cache' : '🔄 Fresh query'}
        </div>
      `, 'bot');
    }
  } catch (error) {
    addMessage(`Network error: ${error.message}`, 'bot', 'error');
  }
}

function addMessage(content, sender, type = 'normal') {
  const chatBox = document.getElementById("chat-box");
  const now = new Date();
  const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  const messageEl = document.createElement('div');
  messageEl.className = `msg ${sender}`;
  
  let bubbleClass = '';
  if (type === 'error') bubbleClass = 'error-bubble';
  else if (type === 'success') bubbleClass = 'success-bubble';
  
  messageEl.innerHTML = `
    ${sender === 'bot' ? '<div class="bot-avatar"><i class="fas fa-robot"></i></div>' : ''}
    <div class="msg-bubble ${bubbleClass}">
      ${content}
      <span class="msg-time">${timeString}</span>
    </div>
    ${sender === 'user' ? '<div class="user-avatar"><i class="fas fa-user"></i></div>' : ''}
  `;
  
  chatBox.appendChild(messageEl);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
  const chatBox = document.getElementById("chat-box");
  const typingId = 'typing-' + Date.now();
  
  const typingEl = document.createElement('div');
  typingEl.className = 'msg bot typing';
  typingEl.id = typingId;
  
  typingEl.innerHTML = `
    <div class="bot-avatar"><i class="fas fa-robot"></i></div>
    <div class="msg-bubble">
      <div class="typing-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  `;
  
  chatBox.appendChild(typingEl);
  chatBox.scrollTop = chatBox.scrollHeight;
  
  return typingId;
}

function removeTypingIndicator(id) {
  const typingEl = document.getElementById(id);
  if (typingEl) {
    typingEl.remove();
  }
}

function formatData(data) {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return '<p>No data returned</p>';
  }
  
  // If it's a simple array of values
  if (!Array.isArray(data[0]) && typeof data[0] !== 'object') {
    return `<ul>${
      data.map(item => `<li>${JSON.stringify(item)}</li>`).join('')
    }</ul>`;
  }
  
  // If it's an array of objects (most common case)
  const headers = Object.keys(data[0]);
  const rows = data.map(row => Object.values(row));
  
  return `
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>${
            headers.map(header => `<th>${header}</th>`).join('')
          }</tr>
        </thead>
        <tbody>${
          rows.map(row => `
            <tr>${
              row.map(cell => `<td>${cell !== null ? cell : '<em>null</em>'}</td>`).join('')
            }</tr>
          `).join('')
        }</tbody>
      </table>
    </div>
  `;
}

// Event listeners
document.getElementById("user-input").addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

// Focus input on page load
window.addEventListener('load', () => {
  document.getElementById("user-input").focus();
});