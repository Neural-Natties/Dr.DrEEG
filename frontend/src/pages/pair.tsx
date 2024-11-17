import { useRouter } from 'next/router';

const PairingPage = () => {
  const router = useRouter();

  return (
    <div className='flex flex-col justify-center z-[1] items-center h-screen !overflow-y-scroll'>
      <div className='flex flex-col justify-center text-center items-center pt-4'>
        <h1 className='text-4xl font-bold text-black mb-6 w-full'>
          Set Up Your Muse-S Device
        </h1>
        <p className='text-xl text-gray-700 mb-4 text-center max-w-2xl justify-center'>
          Follow these simple steps to connect your Muse-S device to Dr. DrEEG
          and start enjoying personalized karaoke!
        </p>
      </div>
      <div className='relative flex flex-row z-[1]'>
        <div className='flex flex-col items-center p-6'>
          <div className='bg-white rounded-lg shadow-lg p-6 w-full max-w-xl'>
            <h2 className='text-2xl font-semibold text-blue-600 mb-4'>
              Step 1: Turn On Your Muse-S
            </h2>
            <p className='text-lg text-gray-700 mb-6'>
              Press and hold the power button on your Muse-S device until the
              LED light starts flashing blue. This means the device is ready to
              pair.
            </p>

            <h2 className='text-2xl font-semibold text-blue-600 mb-4'>
              Step 2: Enable Bluetooth
            </h2>
            <p className='text-lg text-gray-700 mb-6'>
              Make sure Bluetooth is enabled on your device (phone or computer).
              Open the Bluetooth settings and look for your Muse-S device in the
              available devices list.
            </p>

            <h2 className='text-2xl font-semibold text-blue-600 mb-4'>
              Step 3: Pair the Device
            </h2>
            <p className='text-lg text-gray-700 mb-6'>
              Select your Muse-S device from the list of available Bluetooth
              devices. If prompted, confirm the pairing by pressing the pairing
              button on your Muse-S.
            </p>

            <h2 className='text-2xl font-semibold text-blue-600 mb-4'>
              Step 4: Confirm Connection
            </h2>
            <p className='text-lg text-gray-700 mb-6'>
              Once paired, you should see a solid blue LED light on your Muse-S.
              This means your device is now connected to Dr. DrEEG and ready to
              start reading your brain waves.
            </p>

            <h2 className='text-2xl font-semibold text-blue-600 mb-4'>
              Step 5: Start Singing!
            </h2>
            <p className='text-lg text-gray-700 mb-6'>
              With your Muse-S connected, return to Dr. DrEEG and click{' '}
              <span className='text-blue-600 font-semibold'>Start Karaoke</span>{' '}
              to begin your karaoke experience. Your brain waves will guide the
              song selection, ensuring you get the perfect song for your mood.
            </p>
          </div>
        </div>
        <div className='flex flex-col items-center p-6'>
          <div className='bg-white rounded-lg shadow-lg p-6 w-full max-w-xl'>
            <button
              className='mt-6 px-6 py-2 bg-blue-500 text-white text-xl rounded hover:bg-blue-600 disabled:bg-neutral-300'
              onClick={() => router.push('/karaoke')}
            >
              Start Karaoke
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PairingPage;
