import { useState } from 'react';
import { WebSocketMessage } from '../types';

export const useWebSocket = (url: string) => {
  const [data, setData] = useState<WebSocketMessage | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const ws = new WebSocket(url);

  ws.onopen = () => {
    setIsConnected(true);
  };
  return ws;
};
