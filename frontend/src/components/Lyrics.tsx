import { useEffect, useState } from 'react';

interface LyricsProps {
  lyrics?: string[];
  interval?: number;
}

export const Lyrics: React.FC<LyricsProps> = ({ lyrics, interval = 3000 }) => {
  const [currentLyricIndex, setCurrentLyricIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      if (lyrics?.length) {
        setCurrentLyricIndex((prev) =>
          prev + 1 >= lyrics.length ? 0 : prev + 1
        );
      }
    }, interval);

    return () => clearInterval(timer);
  }, [lyrics, interval]);

  return (
    <div className='h-64 flex flex-col items-center justify-center'>
      {lyrics
        ?.slice(currentLyricIndex, currentLyricIndex + 5)
        .map((line, index) => (
          <p
            key={currentLyricIndex + index}
            className='text-3xl text-center my-4 transition-all duration-500'
            style={{
              opacity: index === 2 ? 1 : 0.3,
              transform: `scale(${index === 2 ? 1.1 : 1})`,
              color: index === 2 ? '#ffffff' : '#808080',
            }}
          >
            {line}
          </p>
        ))}
    </div>
  );
};
