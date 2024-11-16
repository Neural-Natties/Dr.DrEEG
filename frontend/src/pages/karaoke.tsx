import { useWebSocket } from '@/hooks/useWebSocket';
import React from 'react';
import { useSpotifyAuth } from '@/hooks/useAuth'

const KaraokePage: React.FC = () => {
  const { data, isConnected } = useWebSocket('ws://localhost:8000/ws');

  const token = useSpotifyAuth()

  return (
    <div className='p-6 text-2xl w-screen h-screen'>
      <h1>WebSocket Messages</h1>
      <p>Status: {isConnected ? 'Connected' : 'Disconnected'}</p>
      <ul>
        <li>{JSON.stringify(data)}</li>
      </ul>
    </div>
  );
};

export default KaraokePage;