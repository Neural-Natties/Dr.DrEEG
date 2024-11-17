import React, { useEffect, useState } from 'react';

interface WebPlaybackProps {
  token: string;
  onPlayerReady: (deviceId: string) => void;
  onPlaybackChange?: (isPlaying: boolean) => void;
  onTrackChange?: () => void;
}

const WebPlayback: React.FC<WebPlaybackProps> = ({
  token,
  onPlayerReady,
  onPlaybackChange,
  onTrackChange,
}) => {
  const [is_paused, setPaused] = useState(false);
  const [is_active, setActive] = useState(false);
  const [player, setPlayer] = useState<Spotify.Player | undefined>(undefined);
  const [current_track, setTrack] = useState({
    id: '',
    name: '',
    album: { images: [{ url: '' }] },
    artists: [{ name: '' }],
    duration_ms: 0,
  });
  const [volume, setVolume] = useState(50);
  const [position, setPosition] = useState(0);
  const [previousPosition, setPreviousPosition] = useState(0);

  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://sdk.scdn.co/spotify-player.js';
    script.async = true;
    document.body.appendChild(script);

    window.onSpotifyWebPlaybackSDKReady = () => {
      const player = new window.Spotify.Player({
        name: 'HugAI Karaoke',
        getOAuthToken: (cb) => {
          cb(token);
        },
        volume: volume / 100,
      });

      setPlayer(player);

      player.addListener('ready', ({ device_id }) => {
        fetch('https://api.spotify.com/v1/me/player', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            device_ids: [device_id],
          }),
        }).then(() => onPlayerReady(device_id));
      });

      player.addListener('player_state_changed', (state) => {
        if (!state) return;

        // Track change detection
        const isNewTrack =
          state.track_window.current_track.id !== current_track.id;
        // Track end detection (position resets to 0 and was previously playing)
        const isTrackEnd = state.position === 0 && previousPosition > 0;

        if (isNewTrack || isTrackEnd) {
          setTrack({
            id: state.track_window.current_track.id || '',
            name: state.track_window.current_track.name,
            album: {
              images: state.track_window.current_track.album.images,
            },
            artists: state.track_window.current_track.artists,
            duration_ms: state.track_window.current_track.duration_ms,
          });
          onTrackChange?.();
        }

        setPreviousPosition(state.position);
        setPaused(state.paused);
        setPosition(state.position);
        onPlaybackChange?.(!state.paused);

        player.getCurrentState().then((state) => {
          !state ? setActive(false) : setActive(true);
        });
      });

      player.connect();
    };
  }, [token]);

  useEffect(() => {
    if (!player || !is_active) return;

    const interval = setInterval(() => {
      player.getCurrentState().then((state) => {
        if (state) {
          setPosition(state.position);
        }
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [player, is_active]);

  useEffect(() => {
    if (player) {
      player.setVolume(volume / 100);
    }
  }, [volume, player]);

  const handleSeek = (value: number) => {
    player?.seek(value).then(() => {
      setPosition(value);
    });
  };

  const formatTime = (ms: number) => {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className='fixed bottom-0 left-0 right-0 p-4 bg-black/50 backdrop-blur-lg z-50'>
      <div className='flex flex-col max-w-4xl mx-auto gap-2'>
        <div className='flex items-center justify-between'>
          <div className='flex items-center gap-4'>
            <div className='text-white'>
              <div className='font-bold'>{current_track.name}</div>
              <div className='text-sm text-gray-300'>
                {current_track.artists[0].name}
              </div>
            </div>
          </div>

          <div className='flex items-center gap-6'>
            <button
              className='text-white hover:text-green-400 transition-colors text-2xl'
              onClick={() => {
                onTrackChange?.();
                player?.previousTrack();
              }}
            >
              ⏮
            </button>
            <button
              className='text-white hover:text-green-400 transition-colors text-3xl'
              onClick={() => player?.togglePlay()}
            >
              {is_paused ? '▶' : '⏸'}
            </button>
            <button
              className='text-white hover:text-green-400 transition-colors text-2xl'
              onClick={() => {
                onTrackChange?.();
                player?.nextTrack();
              }}
            >
              ⏭
            </button>
          </div>

          <div className='flex items-center gap-2'>
            <span className='text-white'>🔈</span>
            <input
              type='range'
              min='0'
              max='100'
              value={volume}
              onChange={(e) => setVolume(Number(e.target.value))}
              className='w-24'
            />
          </div>
        </div>

        <div className='flex items-center gap-2'>
          <span className='text-white text-sm'>{formatTime(position)}</span>
          <input
            type='range'
            min='0'
            max={current_track.duration_ms}
            value={position}
            onChange={(e) => handleSeek(Number(e.target.value))}
            className='flex-grow'
          />
          <span className='text-white text-sm'>
            {formatTime(current_track.duration_ms)}
          </span>
        </div>
      </div>
    </div>
  );
};

export default WebPlayback;
