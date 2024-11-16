import React, { useEffect, useState } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';

const HomePage: React.FC = () => {
  const { data, isConnected } = useWebSocket("ws://localhost:8000/wstest");

  return (
    <div className='p-6 text-2xl'>
      <h1>WebSocket Messages</h1>
      <p>Status: {isConnected ? 'Connected' : 'Disconnected'}</p>
      <ul>
        <li>{JSON.stringify(data)}</li>
      </ul>
    </div>
  );
};

export default HomePage;
