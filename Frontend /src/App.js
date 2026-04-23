import React, { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        message: message,
      });

      const newChat = [
        ...chatHistory,
        { sender: "user", text: message },
        { sender: "bot", text: res.data.response },
      ];

      setChatHistory(newChat);
      setMessage("");
    } catch (error) {
      const newChat = [
        ...chatHistory,
        { sender: "user", text: message },
        { sender: "bot", text: "❌ Error connecting to backend" },
      ];
      setChatHistory(newChat);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>AI CRM - HCP Module</h1>

      <div style={styles.chatBox}>
        {chatHistory.map((chat, index) => (
          <div
            key={index}
            style={
              chat.sender === "user"
                ? styles.userMessage
                : styles.botMessage
            }
          >
            {chat.text}
          </div>
        ))}
      </div>

      <div style={styles.inputContainer}>
        <input
          style={styles.input}
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        <button style={styles.button} onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    fontFamily: "Arial",
    padding: "20px",
    maxWidth: "600px",
    margin: "auto",
  },
  title: {
    textAlign: "center",
  },
  chatBox: {
    border: "1px solid #ccc",
    borderRadius: "10px",
    padding: "10px",
    height: "400px",
    overflowY: "auto",
    marginBottom: "10px",
    backgroundColor: "#f9f9f9",
  },
  userMessage: {
    textAlign: "right",
    margin: "5px",
    padding: "8px",
    backgroundColor: "#d1e7dd",
    borderRadius: "10px",
  },
  botMessage: {
    textAlign: "left",
    margin: "5px",
    padding: "8px",
    backgroundColor: "#f8d7da",
    borderRadius: "10px",
  },
  inputContainer: {
    display: "flex",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ccc",
  },
  button: {
    marginLeft: "10px",
    padding: "10px 20px",
    border: "none",
    backgroundColor: "#007bff",
    color: "white",
    borderRadius: "5px",
    cursor: "pointer",
  },
};

export default App;

