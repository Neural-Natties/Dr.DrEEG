import { SpotlightLoader } from '@/components/Loading';
import { Lyrics } from '@/components/Lyrics';
import WebPlayback from '@/components/WebPlayback';
import { useSpotifyAuth } from '@/hooks/useAuth';
import { Scene } from '@/scenes/Scene';
import { WebSocketMessage } from '@/types';
import { Canvas } from '@react-three/fiber';
import React, { useEffect, useState } from 'react';

const KaraokePage: React.FC = () => {
  const token = useSpotifyAuth().token;
  const [isConnected, setIsConnected] = useState(false);
  const [data, setData] = useState<WebSocketMessage | null>(null);
  const [deviceId, setDeviceId] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [currentTrackId, setCurrentTrackId] = useState<string | null>(null);
  const [isFinished, setIsFinished] = useState(false);

  const requestUpdate = () => {
    fetch('http://localhost:8000/song')
      .then((data) => data.json())
      .then((data) => {
        setData(data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setIsFinished(false);
        setIsLoading(false);
      });
  };
  useEffect(() => {}, [data]);

  useEffect(() => {
    if (!isConnected) {
      setIsConnected(true);
      requestUpdate();
    }
  }, [isConnected]);

  useEffect(() => {
    if (isFinished) {
      requestUpdate();
    }
  }, [isFinished]);

  useEffect(() => {
    if (
      !data?.song?.id ||
      !token ||
      !deviceId ||
      data.song.id === currentTrackId
    )
      return;

    setIsLoading(true);
    setCurrentTrackId(data.song.id);

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
      .then(() => {
        setIsPlaying(true);
        setTimeout(() => setIsLoading(false), 1000);
      })
      .catch((error) => {
        console.error(error);
        setIsLoading(false);
      });
  }, [data?.song?.id, token, deviceId, currentTrackId]);

  const handleTrackChange = () => {
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 1000);
  };

  if (!data?.song) {
    return (
      <div className='relative w-screen h-screen'>
        <Canvas className='absolute inset-0 bg-black'>
          <SpotlightLoader />
        </Canvas>
      </div>
    );
  }

  return (
    <div className='relative w-screen h-screen'>
      <Canvas className={`absolute inset-0 bg-black`}>
        {isLoading ? (
          <SpotlightLoader />
        ) : (
          <Scene albumArt={data.song.albumArt || ''} />
        )}
      </Canvas>

      <div className='absolute inset-0 flex flex-col items-center justify-center'>
        {!isLoading && (
          <>
            <div className='z-10 w-full max-w-4xl mt-48'>
              <Lyrics
                lyrics={data.song.lyrics}
                isPlaying={isPlaying && !isLoading}
              />
            </div>
          </>
        )}
      </div>

      {token && (
        <WebPlayback
          token={token}
          onPlayerReady={setDeviceId}
          onFinished={handleTrackChange}
          sendMessage={requestUpdate}
          onPlaybackChange={setIsPlaying}
          setLoading={setIsLoading}
        />
      )}
    </div>
  );
};

export default KaraokePage;
