import { OrbitControls, Stars } from '@react-three/drei';
import { useFrame, useLoader } from '@react-three/fiber';
import { useRef } from 'react';
import { TextureLoader } from 'three';

function AlbumArtVisualizer({ albumArt }: { albumArt: string }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const texture = useLoader(TextureLoader, albumArt);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.005;
      meshRef.current.position.y =
        1.3 + Math.sin(state.clock.elapsedTime) * 0.2;
    }
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[2, 2, 0.1]} />
      <meshStandardMaterial
        map={texture}
        emissive='#ffffff'
        emissiveIntensity={0.1}
        metalness={0.8}
        roughness={0.2}
      />
    </mesh>
  );
}

export function Scene({ albumArt }: { albumArt: string }) {
  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      <Stars radius={100} depth={50} count={5000} factor={4} />
      <AlbumArtVisualizer albumArt={albumArt} />
      <OrbitControls enableZoom={false} enablePan={false} />
    </>
  );
}
