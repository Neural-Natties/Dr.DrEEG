import { Lyrics } from '@/components/Lyrics';
import WebPlayback from '@/components/WebPlayback';
import { useSpotifyAuth } from '@/hooks/useAuth';
import { useWebSocket } from '@/hooks/useWebSocket';

const KaraokePage: React.FC = () => {
  const { data } = useWebSocket('ws://localhost:8000/ws');
  const token = useSpotifyAuth().token!;

  return (
    <div className='flex flex-col items-center justify-center min-h-screen bg-black text-white p-6 relative'>
      {data?.song && (
        <>
          <img
            src={data.song.albumArt || undefined}
            alt='Album Art'
            className='w-[24rem] h-[24rem] rounded-2xl shadow-2xl mb-5 z-10'
          />
          <h2 className='text-2xl font-bold mb-2 z-10'>{data.song.name}</h2>
          <p className='text-xl mb-12 text-gray-300 z-10'>{data.song.artist}</p>
          <div className='z-10 w-full max-w-4xl'>
            <Lyrics lyrics={data.song.lyrics} />
          </div>
        </>
      )}
      {!token ? <p>loading</p> : <WebPlayback token={token} />}
    </div>
  );
};

export default KaraokePage;
