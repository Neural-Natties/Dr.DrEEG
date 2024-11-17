import { useWebSocket } from '@/hooks/useWebSocket';
import React, { useEffect, useState } from 'react';
import { useSpotifyAuth } from '@/hooks/useAuth';
import WebPlayback from '@/components/WebPlayback';


const KaraokePage: React.FC = () => {
  const { data, isConnected } = useWebSocket('ws://localhost:8000/ws');
  const token = useSpotifyAuth().token!;

  return (
    <div className='p-6 text-2xl w-screen h-screen'>
      <h1>WebSocket Messages</h1>
      <p>Status: {isConnected ? 'Connected' : 'Disconnected'}</p>
      {!token ? <p>loading</p> : <WebPlayback token={token} />}
    </div>
  );
};

export default KaraokePage;
