import { Text } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import { useMemo, useRef } from 'react';
import { SpotLight } from 'three';

export const SpotlightLoader = () => {
  const lightRef = useRef<SpotLight>(null!);
  const speed = useMemo(() => Math.random() * 0.5 + 0.5, []);
  const positionOffset = useMemo(
    () => ({
      x: Math.random() * 100,
      y: Math.random() * 100,
      z: Math.random() * 100,
    }),
    []
  );

  useFrame(({ clock }) => {
    if (lightRef.current) {
      const t = clock.getElapsedTime() * speed;
      lightRef.current.position.x = Math.sin(t + positionOffset.x) * 5;
      lightRef.current.position.y = Math.cos(t + positionOffset.y) * 5;
      lightRef.current.position.z = Math.sin(t + positionOffset.z) * 5;
    }
  });

  return (
    <>
      <Text
        position={[0, 0, 0]}
        fontSize={1}
        color='#ffffff'
        anchorX='center'
        anchorY='middle'
      >
        loading
      </Text>
      <spotLight
        ref={lightRef}
        position={[0, 5, 0]}
        angle={0.5}
        penumbra={1}
        intensity={2}
        castShadow
      />
    </>
  );
};
