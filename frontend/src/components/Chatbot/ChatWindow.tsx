import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './ChatWindow.module.css';

interface ChatWindowProps {
  isOpen: boolean;
  onToggle: () => void;
}

interface Message {
  sender: 'user' | 'ai';
  text: string;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ isOpen, onToggle }) => {
  const { siteConfig } = useDocusaurusContext();
  const apiUrl = (siteConfig.customFields?.apiUrl as string) || 'http://localhost:8000';

  const [messages, setMessages] = useState<Message[]>([
    { sender: 'ai', text: 'Hi there! How can I help you with the AI Powered Book today?' },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (!isOpen) {
    return null;
  }

  const handleSendMessage = async () => {
    if (inputMessage.trim() === '') return;

    const userMessage: Message = { sender: 'user', text: inputMessage };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputMessage('');

    try {
      const response = await fetch(`${apiUrl}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage.text }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const aiMessage: Message = { sender: 'ai', text: data.response };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = { sender: 'ai', text: 'Sorry, I am having trouble connecting to the AI assistant.' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className={styles.chatWindow}>
      <div className={styles.chatHeader}>
        <h3>AI Assistant</h3>
        <button onClick={onToggle} className={styles.chatCloseButton}>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        </button>
      </div>
      <div className={styles.chatMessages}>
        {messages.map((msg, index) => (
          <div
            key={index}
            className={clsx(styles.message, {
              [styles.userMessage]: msg.sender === 'user',
              [styles.aiMessage]: msg.sender === 'ai',
            })}
          >
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className={styles.chatInputContainer}>
        <input
          type="text"
          placeholder="Type your message..."
          className={styles.chatInput}
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button onClick={handleSendMessage} className={styles.sendButton}>Send</button>
      </div>
    </div>
  );
};

export default ChatWindow;