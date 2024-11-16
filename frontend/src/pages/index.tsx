import React from 'react';
import { useRouter } from "next/router";

const HomePage: React.FC = () => {

  const router = useRouter();

  return (
    <div className="relative z-[1]">
      <div className="flex flex-col justify-center items-center min-h-screen">
        <h1 className="text-7xl font-bold text-black">Dr. DrEEG</h1>
        <p className="mt-4 text-lg text-gray-700 text-center max-w-xl">
          A karaoke website that reads your brain waves and picks the perfect song for you to sing!
        </p>
        <button className="mt-6 px-4 py-2 bg-blue-500 text-white text-xl rounded hover:bg-blue-600" onClick={() => router.push('/pair')}>
          Get Started
        </button>
      </div>
      <div className="flex flex-col items-center mt-16 px-6">
        <h2 className="text-4xl font-bold text-black mb-4">Why Dr. DrEEG?</h2>
        <p className="text-lg text-gray-700 text-center max-w-3xl">
          Dr. DrEEG offers a revolutionary way to experience karaoke. By analyzing your brain waves,
          it personalizes song choices that resonate with your current mood and energy. Whether you're
          feeling upbeat, nostalgic, or looking to blow off some steam, Dr. DrEEG ensures every performance
          is uniquely *you*. Sing smarter, not harder!
        </p>
      </div>
    </div>
  );
};

export default HomePage;
