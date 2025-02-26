import { useRouter } from 'next/router';

const PairingStep = ({
  number,
  title,
  description,
}: {
  number: number;
  title: string;
  description: string;
}) => (
  <div className='mb-8'>
    <h2 className='text-2xl font-semibold text-white mb-4 flex items-center gap-3'>
      <span className='bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center'>
        {number}
      </span>
      {title}
    </h2>
    <p className='text-lg text-white/90'>{description}</p>
  </div>
);

const PairingPage = () => {
  const router = useRouter();

  const steps = [
    {
      title: 'Turn On Your Muse-S',
      description:
        'Press and hold the power button on your Muse-S device until the LED light starts flashing blue. This means the device is ready to pair.',
    },
    {
      title: 'Enable Bluetooth',
      description:
        'Make sure Bluetooth is enabled on your device. Open the Bluetooth settings and look for your Muse-S device in the available devices list.',
    },
    {
      title: 'Pair the Device',
      description:
        'Select your Muse-S device from the list of available Bluetooth devices. If prompted, confirm the pairing by pressing the pairing button on your Muse-S.',
    },
    {
      title: 'Confirm Connection',
      description:
        'Once paired, you should see a solid blue LED light on your Muse-S. This means your device is now connected to Dr. DrEEG and ready to start reading your brain waves.',
    },
    {
      title: 'Start Singing!',
      description:
        'With your Muse-S connected, click Start Karaoke to begin your personalized karaoke experience. Your brain waves will guide the song selection for your perfect mood.',
    },
  ];

  return (
    <div className='relative overflow-scroll w-screen h-screen bg-gradient-to-br from-blue-900 to-black'>
      <div className='absolute inset-0 bg-black/40'></div>
      <div className='relative z-10 max-w-4xl mx-auto py-12 px-4'>
        <div className='text-center mb-12'>
          <h1 className='text-4xl font-bold text-white mb-4'>
            Set Up Your Muse-S Device
          </h1>
          <p className='text-xl text-white/90'>
            Follow these simple steps to connect your Muse-S device and start
            enjoying personalized karaoke!
          </p>
        </div>

        <div className='bg-black/50 backdrop-blur-sm rounded-2xl shadow-xl p-6 mb-6'>
          {steps.map((step, index) => (
            <PairingStep
              key={index}
              number={index + 1}
              title={step.title}
              description={step.description}
            />
          ))}
        </div>

        <div className='text-center'>
          <button
            className='px-8 py-3 bg-blue-600 text-white text-xl rounded-lg
              hover:bg-blue-500 transform hover:scale-105 transition-all
              shadow-lg hover:shadow-xl disabled:bg-neutral-300'
            onClick={() => router.push('/karaoke')}
          >
            Start Karaoke
          </button>
        </div>
      </div>
    </div>
  );
};

export default PairingPage;
