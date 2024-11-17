import { Lyrics } from '@/components/Lyrics';
import WebPlayback from '@/components/WebPlayback';
import { useSpotifyAuth } from '@/hooks/useAuth';
import { useWebSocket } from '@/hooks/useWebSocket';
import { Scene } from '@/scenes/Scene';
import { Canvas } from '@react-three/fiber';
import React, { useEffect, useState } from 'react';

const KaraokePage: React.FC = () => {
  const { data } = useWebSocket('ws://localhost:8000/ws');
  const token = useSpotifyAuth().token;
  const [deviceId, setDeviceId] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (!data || !token || !deviceId) return;

    fetch('https://api.spotify.com/v1/me/player/play?device_id=' + deviceId, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        uris: [`spotify:track:${data.song.id}`],
        position_ms: 0,
      }),
    })
      .then(() => setIsPlaying(true))
      .catch(console.error);
  }, [data, token, deviceId]);

  return (
    <div className='relative w-screen h-screen'>
      <Canvas className='absolute inset-0 bg-black'>
        {data?.song?.albumArt && <Scene albumArt={data.song.albumArt} />}
      </Canvas>

      <div className='absolute inset-0 flex flex-col items-center justify-center'>
        {data?.song && (
          <>
            <div className='z-10 w-full max-w-4xl mt-48'>
              <Lyrics lyrics={data.song.lyrics} isPlaying={isPlaying} />
            </div>
          </>
        )}
      </div>

      {!token ? (
        <div className='absolute bottom-0 w-full text-center p-4 text-white'>
          Loading...
        </div>
      ) : (
        <WebPlayback
          token={token}
          onPlayerReady={setDeviceId}
          onPlaybackChange={setIsPlaying}
        />
      )}
    </div>
  );
};

export default KaraokePage;
