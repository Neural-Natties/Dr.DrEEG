import { Text } from '@react-three/drei';
import { useFrame, useThree } from '@react-three/fiber';
import { useRef, useState } from 'react';
import { Group, Mesh, Vector3 } from 'three';

export const LoadingTransition = () => {
  const groupRef = useRef<Group>(null);
  const sphereRef = useRef<Mesh>(null);
  const ringRef = useRef<Mesh>(null);
  const [hovered, setHovered] = useState(false);
  const [clicked, setClicked] = useState(false);
  const { mouse, viewport } = useThree();

  useFrame((state) => {
    if (!groupRef.current) return;

    // Follow mouse movement
    const x = (mouse.x * viewport.width) / 2;
    const y = (mouse.y * viewport.height) / 2;
    groupRef.current.position.lerp(new Vector3(x, y, 0), 0.1);

    // Rotation effects
    groupRef.current.rotation.y += clicked ? 0.02 : 0.005;

    if (sphereRef.current) {
      sphereRef.current.rotation.x += 0.01;
      sphereRef.current.rotation.y += 0.01;
      const scale = 0.5 + Math.sin(state.clock.elapsedTime * 2) * 0.1;
      const boost = hovered ? 1.2 : 1;
      sphereRef.current.scale.set(scale * boost, scale * boost, scale * boost);
    }

    if (ringRef.current) {
      ringRef.current.rotation.x -= clicked ? 0.01 : 0.002;
      ringRef.current.rotation.z += clicked ? 0.01 : 0.002;
    }
  });

  return (
    <group
      ref={groupRef}
      onClick={() => setClicked(!clicked)}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <mesh ref={sphereRef}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial
          color={hovered ? '#23ff6d' : '#1DB954'}
          emissive={clicked ? '#23ff6d' : '#1DB954'}
          emissiveIntensity={hovered ? 0.8 : 0.5}
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>

      <mesh ref={ringRef}>
        <torusGeometry args={[1, 0.05, 16, 100]} />
        <meshStandardMaterial
          color={hovered ? '#23ff6d' : '#1DB954'}
          emissive={clicked ? '#23ff6d' : '#1DB954'}
          emissiveIntensity={hovered ? 0.5 : 0.3}
          transparent
          opacity={0.6}
        />
      </mesh>

      <Text
        position={[0, -1.5, 0]}
        fontSize={0.25}
        color={hovered ? '#23ff6d' : '#1DB954'}
        anchorX='center'
        anchorY='middle'
      >
        {clicked ? 'Loading...' : 'Click me!'}
      </Text>

      <pointLight position={[5, 5, 5]} intensity={hovered ? 1.5 : 1} />
      <ambientLight intensity={0.4} />
    </group>
  );
};
