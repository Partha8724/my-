"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { Float, OrbitControls, RoundedBox } from "@react-three/drei";
import { useRef } from "react";
import type { Group, Mesh, MeshStandardMaterial } from "three";

type BlockProps = {
  position: [number, number, number];
  size: [number, number, number];
  color: string;
  opacity?: number;
};

function GlassBlock({ position, size, color, opacity = 0.2 }: BlockProps) {
  return (
    <RoundedBox position={position} args={size} radius={0.05} smoothness={5}>
      <meshPhysicalMaterial
        color={color}
        transparent
        opacity={opacity}
        transmission={0.92}
        thickness={0.55}
        roughness={0.08}
        metalness={0.05}
        ior={1.15}
        clearcoat={1}
        clearcoatRoughness={0.12}
        emissive={color}
        emissiveIntensity={0.25}
      />
    </RoundedBox>
  );
}

function PrismArchitecture() {
  const architecture = useRef<Group>(null);

  useFrame((_, delta) => {
    if (architecture.current) architecture.current.rotation.y += delta * 0.14;
  });

  return (
    <Float speed={1.15} rotationIntensity={0.18} floatIntensity={0.65}>
      <group ref={architecture}>
        <GlassBlock position={[0, -1.22, 0]} size={[3.4, 0.14, 2.5]} color="#36d4ff" opacity={0.3} />
        <GlassBlock position={[0, -1.08, 0]} size={[2.8, 0.1, 2]} color="#8b5cf6" opacity={0.22} />

        <GlassBlock position={[0, -0.55, 0]} size={[1.9, 0.55, 1.4]} color="#67e8f9" />
        <GlassBlock position={[0, 0.2, 0]} size={[1.45, 0.5, 1.05]} color="#f472b6" />
        <GlassBlock position={[0, 0.86, 0]} size={[1.02, 0.36, 0.82]} color="#f59e0b" opacity={0.24} />

        <GlassBlock position={[-1.05, -0.42, -0.22]} size={[0.55, 0.88, 0.55]} color="#22d3ee" opacity={0.26} />
        <GlassBlock position={[1.08, -0.38, 0.15]} size={[0.62, 0.95, 0.62]} color="#fb7185" opacity={0.24} />
        <GlassBlock position={[-0.22, -0.72, 0.95]} size={[0.66, 0.3, 0.32]} color="#818cf8" opacity={0.28} />
        <GlassBlock position={[0.84, -0.78, -0.84]} size={[0.54, 0.2, 0.3]} color="#2dd4bf" opacity={0.28} />

        <mesh position={[0, -1.3, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[4.4, 3.2]} />
          <meshStandardMaterial color="#070d26" metalness={0.2} roughness={0.18} />
        </mesh>
      </group>
    </Float>
  );
}

function GlowBars() {
  const bars = useRef<Mesh>(null);

  useFrame(({ clock }) => {
    const material = bars.current?.material as MeshStandardMaterial | undefined;
    if (material) {
      material.emissiveIntensity = 0.25 + Math.sin(clock.elapsedTime * 1.5) * 0.08;
    }
  });

  return (
    <group>
      <mesh ref={bars} position={[0, -1.21, 0.95]}>
        <boxGeometry args={[2.7, 0.03, 0.06]} />
        <meshStandardMaterial color="#f472b6" emissive="#f472b6" emissiveIntensity={0.25} />
      </mesh>
      <mesh position={[-0.9, -1.21, -0.75]} rotation={[0, 0.08, 0]}>
        <boxGeometry args={[1.35, 0.03, 0.06]} />
        <meshStandardMaterial color="#22d3ee" emissive="#22d3ee" emissiveIntensity={0.34} />
      </mesh>
      <mesh position={[0.92, -1.21, -0.64]} rotation={[0, -0.12, 0]}>
        <boxGeometry args={[1.1, 0.03, 0.06]} />
        <meshStandardMaterial color="#facc15" emissive="#facc15" emissiveIntensity={0.3} />
      </mesh>
    </group>
  );
}

export function HeroScene() {
  return (
    <div className="h-[420px] w-full rounded-3xl border border-cyan-200/20 bg-gradient-to-br from-slate-950/80 via-blue-950/60 to-fuchsia-950/60 shadow-[0_0_50px_rgba(56,189,248,0.25)]">
      <Canvas dpr={[1, 1.45]} camera={{ position: [0, 0.15, 4.8], fov: 46 }}>
        <color attach="background" args={["#050919"]} />
        <ambientLight intensity={0.55} />
        <directionalLight position={[3, 4, 3]} intensity={1.6} color="#7dd3fc" />
        <pointLight position={[-2, 1.5, 2]} intensity={20} color="#22d3ee" />
        <pointLight position={[2.5, 0.8, -2]} intensity={18} color="#f472b6" />
        <spotLight position={[0, 4, 0]} angle={0.5} penumbra={0.7} intensity={14} color="#facc15" />
        <PrismArchitecture />
        <GlowBars />
        <OrbitControls enablePan={false} enableZoom={false} autoRotate autoRotateSpeed={0.35} minPolarAngle={1.1} maxPolarAngle={2.1} />
      </Canvas>
    </div>
  );
}
