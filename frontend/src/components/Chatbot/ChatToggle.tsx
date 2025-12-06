import React from 'react';
import clsx from 'clsx';
import styles from './ChatToggle.module.css';

interface ChatToggleProps {
  isOpen: boolean;
  onToggle: () => void;
}

const ChatToggle: React.FC<ChatToggleProps> = ({ isOpen, onToggle }) => {
  return (
    <button
      className={clsx(styles.chatToggleButton, { [styles.chatToggleButtonOpen]: isOpen })}
      onClick={onToggle}
      aria-label="Toggle chat"
    >
      {isOpen ? (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-message-circle-code"><path d="M7.9 20A9 9 0 0 1 4 16c0-4.4 3.6-8 8-8h.4c.7 0 1.5.1 2.2.4"/><path d="m10 10-2 2 2 2"/><path d="m16 10 2 2-2 2"/></svg>
      )}
    </button>
  );
};

export default ChatToggle;