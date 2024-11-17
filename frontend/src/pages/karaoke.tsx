import { Lyrics } from '@/components/Lyrics';
import WebPlayback from '@/components/WebPlayback';
import { useSpotifyAuth } from '@/hooks/useAuth';
import { useWebSocket } from '@/hooks/useWebSocket';
import { Scene } from '@/scenes/Scene';
import { Canvas } from '@react-three/fiber';
import React, { useEffect, useState } from 'react';

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
    <div className='relative w-screen h-screen'>
      <Canvas className='absolute inset-0 bg-black'>
        {data?.song?.albumArt && <Scene albumArt={data.song.albumArt} />}
      </Canvas>

      {!token ? (
        <p className='text-white'>Loading...</p>
      ) : (
        <WebPlayback token={token} onPlayerReady={setDeviceId} />
      )}

      <div className='absolute inset-0 flex flex-col items-center justify-center translate-y-20'>
        {data?.song && (
          <>
            <h2 className='text-2xl font-bold mb-2 z-10 text-white'>
              {data.song.name}
            </h2>
            <p className='text-xl mb-12 text-gray-300 z-10'>
              {data.song.artist}
            </p>
            <div className='z-10 w-full max-w-4xl'>
              <Lyrics lyrics={data.song.lyrics} />
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default KaraokePage;
