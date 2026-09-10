import { useState, useCallback, useRef, useEffect } from 'react';
import { sendMessage } from '../services/api';

const WELCOME_MESSAGE = {
  id: 'welcome',
  sender: 'bot',
  content:
    "Welcome to PrimeHomes Realty.\n\nI'm here to help you find the right property. You can tell me what you're looking for, your preferred location, budget, or whether you're buying or renting.",
};

export function useChat() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [conversationId, setConversationId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const bottomRef = useRef(null);

  // Auto-scroll when messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const send = useCallback(
    async (text) => {
      const trimmed = text.trim();
      if (!trimmed || isLoading) return;

      setError(null);

      // Optimistic customer message
      const tempId = `temp-${Date.now()}`;
      setMessages((prev) => [
        ...prev,
        { id: tempId, sender: 'customer', content: trimmed },
      ]);
      setIsLoading(true);

      try {
        const data = await sendMessage({
          conversationId,
          message: trimmed,
        });

        // Update conversation ID from server
        if (data.conversation_id) {
          setConversationId(data.conversation_id);
        }

        // Append bot reply
        setMessages((prev) => [
          ...prev,
          {
            id: data.message_id || `bot-${Date.now()}`,
            sender: 'bot',
            content: data.reply,
            meta: {
              leadId: data.lead_id,
              status: data.lead_status,
              temperature: data.lead_temperature,
              score: data.score,
              missing: data.missing_information,
            },
          },
        ]);
      } catch (err) {
        setError(err.message || 'Failed to send message');
        // Keep the customer message; show error below
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId, isLoading]
  );

  const retry = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    send,
    retry,
    bottomRef,
    conversationId,
  };
}
