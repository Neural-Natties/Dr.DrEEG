import { useWebSocket } from '@/hooks/useWebSocket';
import React, { use, useEffect, useState } from 'react';
import { useSpotifyAuth } from '@/hooks/useAuth';
import WebPlayback from '@/components/WebPlayback';


const KaraokePage: React.FC = () => {
  const { data, isConnected } = useWebSocket('ws://localhost:8000/ws');
  const token = useSpotifyAuth().token;
  const [deviceId, setDeviceId] = useState<string | null>(null)

  useEffect(() => {
    if (!data || !token || !deviceId) {
      return;
    }
    console.log(data.song.id)
    console.log(token)
    fetch('https://api.spotify.com/v1/me/player/play?device_id=' + deviceId, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ uris: [`spotify:track:${data.song.id}`] }),
    })
  }, [data, token, deviceId]);

  return (
    <div className='p-6 text-2xl w-screen h-screen'>
      <h1>WebSocket Messages</h1>
      <p>Status: {isConnected ? 'Connected' : 'Disconnected'}</p>
      {!token ? <p>loading</p> : <WebPlayback token={token} onPlayerReady={setDeviceId} />}
    </div>
  );
};

export default KaraokePage;
