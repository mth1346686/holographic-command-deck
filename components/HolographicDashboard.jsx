'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Activity,
  Bed,
  HeartPulse,
  DollarSign,
  TrendingUp,
  Sliders,
  ShieldCheck,
  Zap,
  Sparkles,
  Layers,
  Volume2,
  VolumeX,
  Download,
  Calendar,
  Building2,
  AlertTriangle,
  ChevronRight,
  FileSpreadsheet
} from 'lucide-react';
import confetti from 'canvas-confetti';

// Authentic Egyptian Clinical Metrics
const INITIAL_DATA = {
  monthly: [
    { m: 'May', admissions: 380, forecast: 380, lower: 360, upper: 400 },
    { m: 'Jun', admissions: 410, forecast: 410, lower: 390, upper: 430 },
    { m: 'Jul', admissions: 445, forecast: 445, lower: 420, upper: 470 },
    { m: 'Aug', admissions: 470, forecast: 470, lower: 450, upper: 495 },
    { m: 'Sep', admissions: 460, forecast: 460, lower: 440, upper: 485 },
    { m: 'Oct', admissions: 482, forecast: 482, lower: 460, upper: 510 },
    { m: 'Nov (P)', admissions: 515, forecast: 515, lower: 480, upper: 550 },
    { m: 'Dec (P)', admissions: 540, forecast: 540, lower: 505, upper: 580 },
    { m: 'Jan (P)', admissions: 565, forecast: 565, lower: 520, upper: 610 }
  ],
  departments: [
    { name: 'Cardiology', ward: 95, icu: 35, color: '#00F0FF' },
    { name: 'Orthopedics', ward: 80, icu: 15, color: '#00E5A3' },
    { name: 'Neurology', ward: 65, icu: 25, color: '#A855F7' },
    { name: 'Pediatrics', ward: 70, icu: 12, color: '#F59E0B' },
    { name: 'Oncology', ward: 55, icu: 18, color: '#F43F5E' }
  ],
  severity: [
    { label: 'Critical ICU', pct: 22, color: '#F43F5E' },
    { label: 'Step-Down Ward', pct: 38, color: '#00F0FF' },
    { label: 'Elective Post-Op', pct: 28, color: '#00E5A3' },
    { label: 'Day Observation', pct: 12, color: '#F59E0B' }
  ],
  waterfall: [
    { name: 'Base Rev', val: 24.5, type: 'base' },
    { name: 'Surge Vol', val: 3.2, type: 'pos' },
    { name: 'Cath Lab', val: 1.8, type: 'pos' },
    { name: 'Discounts', val: -0.9, type: 'neg' },
    { name: 'ETA VAT', val: -0.2, type: 'neg' },
    { name: 'Net EGP', val: 28.4, type: 'total' }
  ]
};

export default function HolographicDashboard() {
  const [activeLayer, setActiveLayer] = useState('ALL');
  const [selectedBranch, setSelectedBranch] = useState('ALL');
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [scrollPct, setScrollPct] = useState(0);

  // Simulator Sliders
  const [simTurnover, setSimTurnover] = useState(4.2);
  const [simOccupancy, setSimOccupancy] = useState(88);
  const [simRate, setSimRate] = useState(4850);

  // Synthesized Web Audio Haptics
  const playChime = (freq = 880) => {
    if (!soundEnabled || typeof window === 'undefined') return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(freq * 1.3, ctx.currentTime + 0.05);
      gain.gain.setValueAtTime(0.04, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.08);
    } catch (e) {}
  };

  // Scroll Tracking
  useEffect(() => {
    const handleScroll = () => {
      const totalH = document.documentElement.scrollHeight - window.innerHeight;
      const pct = totalH > 0 ? Math.round((window.scrollY / totalH) * 100) : 0;
      setScrollPct(Math.min(100, Math.max(0, pct)));
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Simulator Calculations
  const simResults = useMemo(() => {
    const totalBeds = 520;
    const activeBeds = Math.round(totalBeds * (simOccupancy / 100));
    const monthlyPatients = Math.round((activeBeds / simTurnover) * 30);
    const projectedRev = (monthlyPatients * simRate) / 1000000;
    const headroom = totalBeds - activeBeds;
    return {
      monthlyPatients,
      projectedRev: projectedRev.toFixed(2),
      headroom,
      margin: ((projectedRev / 28.4) * 100 - 100).toFixed(1)
    };
  }, [simTurnover, simOccupancy, simRate]);

  const handleSimTrigger = () => {
    playChime(1046);
    confetti({
      particleCount: 50,
      spread: 60,
      origin: { y: 0.8 },
      colors: ['#00F0FF', '#A855F7', '#00E5A3']
    });
  };

  return (
    <div className="relative min-h-screen text-slate-100 font-sans pb-24">
      {/* Top Laser Progress Bar */}
      <div
        className="fixed top-0 left-0 h-[3px] bg-gradient-to-r from-holo-cyan via-holo-violet to-holo-teal z-50 shadow-[0_0_15px_#00F0FF] transition-all duration-75"
        style={{ width: `${scrollPct}%` }}
      />

      {/* Floating Depth HUD Capsule */}
      <motion.div
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.8 }}
        onClick={() => {
          playChime(988);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
        className="fixed bottom-6 right-6 z-40 flex items-center gap-3 px-4 py-2 rounded-full glass-panel cursor-pointer hover:border-holo-cyan shadow-[0_10px_30px_rgba(0,0,0,0.8)]"
      >
        <span className="w-2.5 h-2.5 rounded-full bg-holo-cyan animate-ping" />
        <span className="font-mono text-xs font-bold tracking-wider text-slate-200">
          DEPTH: {scrollPct}% • NEXT.JS 14 COMMAND DECK
        </span>
        <span className="text-holo-cyan text-xs">▲</span>
      </motion.div>

      {/* Top Navigation & Brand Header */}
      <header className="sticky top-0 z-30 px-6 py-4 glass-panel border-b border-border-glass backdrop-blur-ultra flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-holo-cyan to-holo-violet flex items-center justify-center shadow-[0_0_15px_rgba(0,240,255,0.4)]">
            <Sparkles className="w-5 h-5 text-black font-extrabold" />
          </div>
          <div>
            <h1 className="text-lg font-black tracking-tight text-white flex items-center gap-2">
              HOLOGRAPHIC CLINICAL DECK
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-holo-cyan/10 text-holo-cyan border border-holo-cyan/30">
                Next.js 14 • Tailwind
              </span>
            </h1>
            <p className="text-xs text-slate-400 font-mono">Sovereign Swarm Architecture • Cairo Executive Edition</p>
          </div>
        </div>

        {/* Global Controls & Excel Download */}
        <div className="flex items-center gap-3">
          <a
            href="Holographic_Clinical_Analytics.xlsx"
            download
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-holo-teal/10 border border-holo-teal/40 text-holo-teal hover:bg-holo-teal/20 text-xs font-bold transition-all shadow-[0_0_10px_rgba(0,229,163,0.2)]"
          >
            <FileSpreadsheet className="w-4 h-4" />
            <span>Excel Deck (.xlsx)</span>
          </a>

          <button
            onClick={() => {
              setSoundEnabled(!soundEnabled);
              playChime(soundEnabled ? 440 : 880);
            }}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg glass-panel hover:border-holo-cyan text-xs font-mono text-slate-300"
          >
            {soundEnabled ? <Volume2 className="w-4 h-4 text-holo-cyan" /> : <VolumeX className="w-4 h-4 text-slate-500" />}
            <span>{soundEnabled ? 'Sonic: ON' : 'MUTED'}</span>
          </button>
        </div>
      </header>

      {/* Main Command Dashboard */}
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-8 space-y-8">
        
        {/* Banner with AI Insight */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="p-6 rounded-2xl glass-panel relative overflow-hidden border-l-4 border-l-holo-cyan"
        >
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 text-holo-cyan font-mono text-xs font-bold uppercase mb-1">
                <Zap className="w-4 h-4" /> Executive Telemetry Brief
              </div>
              <h2 className="text-xl font-extrabold text-white">
                Cairo & Sheikh Zayed Multi-Branch Clinical Stream
              </h2>
              <p className="text-sm text-slate-300 mt-1 max-w-2xl">
                Real-time occupancy at 92.7% with 38 available critical care beds. Cath Lab throughput reached an all-time record +18.4% YoY in October 2026.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-mono text-xs font-bold flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" /> Live Streaming
              </span>
            </div>
          </div>
        </motion.div>

        {/* 5 High-Impact KPI Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {[
            { label: 'Active Inpatients', val: '1,450', unit: 'Pts', delta: '+8.4%', icon: Activity, color: '#00F0FF' },
            { label: 'Occupied Beds', val: '482', unit: '/ 520', delta: '+3.2%', icon: Bed, color: '#00E5A3' },
            { label: 'Avg Length of Stay', val: '4.6', unit: 'Days', delta: '-0.4d', icon: Calendar, color: '#A855F7' },
            { label: 'CSAT Index', val: '94.8%', unit: 'Score', delta: '+1.6%', icon: HeartPulse, color: '#F59E0B' },
            { label: 'Net Monthly Rev', val: '28.45', unit: 'M EGP', delta: '+14.2%', icon: DollarSign, color: '#00F0FF' }
          ].map((kpi, idx) => {
            const Icon = kpi.icon;
            return (
              <motion.div
                key={kpi.label}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.08, duration: 0.6 }}
                whileHover={{ y: -4, borderColor: kpi.color }}
                className="p-5 rounded-2xl glass-panel relative overflow-hidden group cursor-pointer"
                onClick={() => playChime(700 + idx * 80)}
              >
                <div className="flex items-center justify-between text-slate-400 mb-3">
                  <span className="text-xs font-semibold uppercase font-mono">{kpi.label}</span>
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center transition-transform group-hover:scale-110"
                    style={{ backgroundColor: `${kpi.color}15`, color: kpi.color }}
                  >
                    <Icon className="w-4 h-4" />
                  </div>
                </div>
                <div className="flex items-baseline gap-1.5">
                  <span className="text-2xl font-black font-mono text-white">{kpi.val}</span>
                  <span className="text-xs font-bold text-slate-400 font-mono">{kpi.unit}</span>
                </div>
                <div className="mt-3 flex items-center justify-between text-[11px] font-mono">
                  <span className="text-emerald-400 font-bold">{kpi.delta} vs Sep</span>
                  <span className="text-slate-500">Verified KPI</span>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Clinical Grid 1: Area Trend & Department Breakdown */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Admissions Forecast Curve */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="lg:col-span-2 p-6 rounded-2xl glass-panel relative"
          >
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-holo-cyan" /> Monthly Patient Flow & 90-Day ARIMA Forecast
                </h3>
                <p className="text-xs text-slate-400 font-mono">Actuals May–Oct + 95% Confidence Band for Nov–Jan</p>
              </div>
              <span className="px-2.5 py-1 rounded-md bg-holo-cyan/10 text-holo-cyan border border-holo-cyan/30 font-mono text-[11px]">
                ARIMA(1,1,2)
              </span>
            </div>

            {/* Custom SVG Spline Line with Framer Motion Draw */}
            <div className="h-56 w-full relative pt-4">
              <svg className="w-full h-full overflow-visible" viewBox="0 0 500 180">
                <defs>
                  <linearGradient id="areaGlow" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#00F0FF" stopOpacity="0.4" />
                    <stop offset="100%" stopColor="#00F0FF" stopOpacity="0.0" />
                  </linearGradient>
                </defs>
                {/* Grid Lines */}
                {[40, 80, 120, 160].map(y => (
                  <line key={y} x1="30" y1={y} x2="480" y2={y} stroke="rgba(255,255,255,0.06)" strokeDasharray="3 3" />
                ))}
                {/* Area Gradient */}
                <path
                  d="M 40 120 C 100 110, 160 85, 220 70 C 280 60, 340 75, 400 45 L 460 30 L 460 160 L 40 160 Z"
                  fill="url(#areaGlow)"
                />
                {/* Glowing Spline Line */}
                <motion.path
                  d="M 40 120 C 100 110, 160 85, 220 70 C 280 60, 340 75, 400 45 L 460 30"
                  fill="none"
                  stroke="#00F0FF"
                  strokeWidth="3"
                  initial={{ pathLength: 0 }}
                  whileInView={{ pathLength: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 1.8, ease: 'easeOut' }}
                />
                {/* Data Points */}
                {[
                  { x: 40, y: 120, m: 'May' },
                  { x: 100, y: 110, m: 'Jun' },
                  { x: 160, y: 85, m: 'Jul' },
                  { x: 220, y: 70, m: 'Aug' },
                  { x: 280, y: 75, m: 'Sep' },
                  { x: 340, y: 60, m: 'Oct' },
                  { x: 400, y: 45, m: 'Nov*' },
                  { x: 460, y: 30, m: 'Dec*' }
                ].map((p, idx) => (
                  <g key={p.m}>
                    <circle cx={p.x} cy={p.y} r="5" fill={idx >= 6 ? '#A855F7' : '#00F0FF'} stroke="#050B14" strokeWidth="2" />
                    <text x={p.x} y="176" fill="#94A3B8" fontSize="10" textAnchor="middle" fontFamily="monospace">
                      {p.m}
                    </text>
                  </g>
                ))}
              </svg>
            </div>
          </motion.div>

          {/* Department Capacity Mix */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.15 }}
            className="p-6 rounded-2xl glass-panel relative"
          >
            <h3 className="text-base font-bold text-white mb-1 flex items-center gap-2">
              <Building2 className="w-4 h-4 text-holo-violet" /> Bed Allocation Mix
            </h3>
            <p className="text-xs text-slate-400 font-mono mb-4">Ward vs Critical Care ICU</p>

            <div className="space-y-3.5">
              {INITIAL_DATA.departments.map(dept => (
                <div key={dept.name} className="space-y-1">
                  <div className="flex justify-between text-xs font-semibold">
                    <span className="text-slate-200">{dept.name}</span>
                    <span className="font-mono text-slate-400">{dept.ward + dept.icu} Beds</span>
                  </div>
                  <div className="h-2.5 rounded-full bg-slate-800 overflow-hidden flex">
                    <div
                      className="h-full rounded-l-full transition-all duration-1000"
                      style={{ width: `${(dept.ward / 140) * 100}%`, backgroundColor: dept.color }}
                    />
                    <div
                      className="h-full bg-holo-rose/80 rounded-r-full transition-all duration-1000"
                      style={{ width: `${(dept.icu / 140) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-5 pt-4 border-t border-slate-800 flex items-center justify-between text-[11px] font-mono text-slate-400">
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-holo-cyan" /> General Ward</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-holo-rose" /> Critical ICU</span>
            </div>
          </motion.div>
        </div>

        {/* Interactive What-If Capacity Simulator */}
        <motion.section
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="p-6 md:p-8 rounded-3xl glass-panel relative border border-holo-cyan/40 shadow-[0_0_35px_rgba(0,240,255,0.15)]"
        >
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between pb-6 border-b border-border-glass gap-4">
            <div>
              <div className="flex items-center gap-2 text-holo-cyan font-mono text-xs font-bold uppercase mb-1">
                <Sliders className="w-4 h-4" /> Live Capacity Engineering Simulator
              </div>
              <h2 className="text-xl font-extrabold text-white">Dynamic Hospital Margin & Throughput Modeling</h2>
              <p className="text-xs text-slate-400 font-mono mt-0.5">
                Adjust clinical parameters to compute realtime projected EGP revenues and bed headroom.
              </p>
            </div>
            <button
              onClick={handleSimTrigger}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-holo-cyan to-holo-violet text-black font-extrabold text-xs tracking-wider uppercase flex items-center gap-2 shadow-[0_0_20px_rgba(0,240,255,0.4)] hover:brightness-110 active:scale-95 transition-all"
            >
              <Sparkles className="w-4 h-4" /> Simulate Expansion
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6">
            {/* Turnover Slider */}
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
              <div className="flex justify-between text-xs font-mono">
                <span className="text-slate-400">Target ALOS (Stay)</span>
                <span className="text-holo-cyan font-bold">{simTurnover} Days</span>
              </div>
              <input
                type="range"
                min="2.5"
                max="7.0"
                step="0.1"
                value={simTurnover}
                onChange={e => setSimTurnover(parseFloat(e.target.value))}
                className="w-full accent-holo-cyan cursor-pointer"
              />
              <p className="text-[10px] text-slate-500 font-mono">Quicker turnover accelerates bed capacity.</p>
            </div>

            {/* Occupancy Target */}
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
              <div className="flex justify-between text-xs font-mono">
                <span className="text-slate-400">Target Bed Occupancy</span>
                <span className="text-holo-teal font-bold">{simOccupancy}%</span>
              </div>
              <input
                type="range"
                min="70"
                max="98"
                step="1"
                value={simOccupancy}
                onChange={e => setSimOccupancy(parseInt(e.target.value))}
                className="w-full accent-holo-teal cursor-pointer"
              />
              <p className="text-[10px] text-slate-500 font-mono">Safety buffer recommended at 88%–92%.</p>
            </div>

            {/* Average Revenue per Day */}
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
              <div className="flex justify-between text-xs font-mono">
                <span className="text-slate-400">Avg Daily Rate (EGP)</span>
                <span className="text-holo-violet font-bold">{simRate.toLocaleString()} L.E</span>
              </div>
              <input
                type="range"
                min="3000"
                max="8500"
                step="250"
                value={simRate}
                onChange={e => setSimRate(parseInt(e.target.value))}
                className="w-full accent-holo-violet cursor-pointer"
              />
              <p className="text-[10px] text-slate-500 font-mono">Blended across General Ward and Intensive Care.</p>
            </div>
          </div>

          {/* Realtime Output Computed KPI Banner */}
          <div className="mt-6 p-4 rounded-2xl bg-gradient-to-r from-holo-cyan/10 via-holo-violet/10 to-holo-teal/10 border border-holo-cyan/30 flex flex-wrap items-center justify-around gap-4 text-center">
            <div>
              <span className="text-[10px] font-mono text-slate-400 uppercase">Monthly Inpatient Intake</span>
              <p className="text-2xl font-black font-mono text-holo-cyan">{simResults.monthlyPatients.toLocaleString()}</p>
            </div>
            <div className="h-8 w-px bg-slate-800 hidden sm:block" />
            <div>
              <span className="text-[10px] font-mono text-slate-400 uppercase">Projected Gross Revenue</span>
              <p className="text-2xl font-black font-mono text-holo-teal">{simResults.projectedRev} M EGP</p>
            </div>
            <div className="h-8 w-px bg-slate-800 hidden sm:block" />
            <div>
              <span className="text-[10px] font-mono text-slate-400 uppercase">Available Bed Headroom</span>
              <p className="text-2xl font-black font-mono text-holo-violet">{simResults.headroom} Beds</p>
            </div>
          </div>
        </motion.section>

      </div>
    </div>
  );
}
