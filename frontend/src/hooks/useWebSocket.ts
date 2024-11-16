import { useState, useEffect } from 'react';
import { WebSocketMessage } from '../types';

export const useWebSocket = () => {
  const [data, setData] = useState<WebSocketMessage | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      setData(JSON.parse(event.data));
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    return () => ws.close();
  }, []);

  return { data, isConnected };
};