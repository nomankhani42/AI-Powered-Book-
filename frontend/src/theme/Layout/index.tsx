import React, {type ReactNode, useState} from 'react';
import Layout from '@theme-original/Layout';
import type LayoutType from '@theme/Layout';
import type {WrapperProps} from '@docusaurus/types';
import ChatToggle from '../../components/Chatbot/ChatToggle'; // Re-import ChatToggle
import ChatWindow from '../../components/Chatbot/ChatWindow';

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): ReactNode {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleToggleChat = () => {
    setIsChatOpen((prev) => !prev);
  };

  return (
    <>
      <Layout {...props} />
      <ChatWindow isOpen={isChatOpen} onToggle={handleToggleChat} />
      {!isChatOpen && <ChatToggle isOpen={isChatOpen} onToggle={handleToggleChat} />} {/* Conditionally render ChatToggle */}
    </>
  );
}
