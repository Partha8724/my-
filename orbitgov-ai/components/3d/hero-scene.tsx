"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { Float, OrbitControls, Torus, MeshDistortMaterial, Text } from "@react-three/drei";
import { useRef } from "react";
import type { Mesh } from "three";

function Orb() {
  const ref = useRef<Mesh>(null);
  useFrame((_, delta) => {
    if (ref.current) ref.current.rotation.y += delta * 0.4;
  });
  return (
    <Float speed={1.5} rotationIntensity={0.8} floatIntensity={1.2}>
      <Torus ref={ref} args={[1.1, 0.28, 32, 120]}>
        <MeshDistortMaterial color="#6AF0F8" distort={0.35} speed={1.8} roughness={0.05} />
      </Torus>
      <Text position={[0, -1.9, 0]} fontSize={0.22} color="#9ec8ff">
        OrbitGov AI
      </Text>
    </Float>
  );
}

export function HeroScene() {
  return (
    <div className="h-[420px] w-full rounded-3xl glass">
      <Canvas dpr={[1, 1.5]} camera={{ position: [0, 0, 4.5], fov: 55 }}>
        <ambientLight intensity={0.8} />
        <pointLight position={[2, 3, 2]} intensity={25} color="#4E8CFF" />
        <Orb />
        <OrbitControls enablePan={false} enableZoom={false} autoRotate autoRotateSpeed={0.7} />
      </Canvas>
    </div>
  );
}
