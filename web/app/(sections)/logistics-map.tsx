"use client";

import { useEffect, useRef, useState } from 'react';
import dynamic from 'next/dynamic';
import type { GlobeMethods } from 'react-globe.gl';

// Dynamically import the Globe component to disable SSR
const Globe = dynamic(() => import('react-globe.gl'), { ssr: false });

// --- Types ---
type RouteStatus = "normal" | "delayed" | "risk";

interface ShippingRoute {
  from: { lat: number; lng: number };
  to: { lat: number; lng: number };
  status: RouteStatus;
}

// --- Sample Data ---
const sampleRoutes: ShippingRoute[] = [
  { from: { lat: 22.3193, lng: 114.1694 }, to: { lat: 34.0522, lng: -118.2437 }, status: "normal" }, // Hong Kong to LA
  { from: { lat: 35.1796, lng: 129.0756 }, to: { lat: 47.6062, lng: -122.3321 }, status: "normal" }, // Busan to Seattle
  { from: { lat: 10.8231, lng: 106.6297 }, to: { lat: 51.9244, lng: 4.4777 }, status: "delayed" }, // Ho Chi Minh to Rotterdam
  { from: { lat: 31.2304, lng: 121.4737 }, to: { lat: 37.7749, lng: -122.4194 }, status: "risk" },    // Shanghai to San Francisco
  { from: { lat: 1.3521, lng: 103.8198 }, to: { lat: 53.5511, lng: 9.9937 }, status: "normal" },     // Singapore to Hamburg
];

// --- Component ---
export default function LogisticsMap() {
  const globeRef = useRef<GlobeMethods | undefined>(undefined);
  const [reduceMotion, setReduceMotion] = useState(false);

  useEffect(() => {
    // Check for prefers-reduced-motion
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduceMotion(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => setReduceMotion(event.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  useEffect(() => {
    if (globeRef.current) {
      // Set initial camera position
      globeRef.current.pointOfView({ lat: 20, lng: 160, altitude: 2.5 });
      
      // Configure controls based on motion preference
      const controls = globeRef.current.controls();
      controls.autoRotate = !reduceMotion;
      controls.autoRotateSpeed = reduceMotion ? 0 : 0.1;
      
      // Limit zoom
      controls.minDistance = 200;
      controls.maxDistance = 600;
    }
  }, [reduceMotion]);
  
  // --- Helper Functions ---
  const getArcColor = (status: RouteStatus) => {
    switch (status) {
      case 'normal': return 'rgba(0, 240, 255, 0.6)'; // Primary Cyan
      case 'delayed': return 'rgba(255, 191, 0, 0.7)'; // Accent Amber
      case 'risk': return 'rgba(255, 100, 150, 0.8)'; // Risk Pink/Red
      default: return 'rgba(255, 255, 255, 0.5)';
    }
  };
  
  return (
    <div className="relative h-full w-full">
      <Globe
        ref={globeRef}
        // --- Globe Imagery ---
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
        
        // --- Background ---
        backgroundColor="rgba(0,0,0,0)" // Transparent
        
        // --- Atmosphere ---
        atmosphereColor="#00F0FF"
        atmosphereAltitude={0.15}
        
        // --- Arcs Data ---
        arcsData={sampleRoutes}
        arcStartLat={(d) => (d as ShippingRoute).from.lat}
        arcStartLng={(d) => (d as ShippingRoute).from.lng}
        arcEndLat={(d) => (d as ShippingRoute).to.lat}
        arcEndLng={(d) => (d as ShippingRoute).to.lng}
        arcColor={(d) => getArcColor((d as ShippingRoute).status)}
        arcStroke={0.3}
        arcDashLength={0.6}
        arcDashGap={0.3}
        arcDashAnimateTime={reduceMotion ? 0 : 1500}
      />
    </div>
  );
}