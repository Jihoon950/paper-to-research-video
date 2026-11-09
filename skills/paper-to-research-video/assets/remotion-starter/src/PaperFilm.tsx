import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import film from '../film.json';

type Kind = 'title' | 'system' | 'problem' | 'method' | 'comparison' | 'result' | 'mechanism' | 'bridge' | 'closing';
type Visual = {left_label?: string; center_label?: string; right_label?: string; left_value?: string; right_value?: string; left_note?: string; right_note?: string; accent?: string};
type SceneData = {id: string; seconds: number; kind: Kind; eyebrow?: string; headline: string; body?: string; caption: string; claim_ids: string[]; asset_ids: string[]; visual?: Visual};
type Asset = {id: string; path: string; kind: string; credit: string; rights: string};

const C = {night: '#132B3D', navy: '#1E3C51', teal: '#138DA0', amber: '#C7773D', paper: '#F5F8F8', line: '#C8D8DE', muted: '#567080', white: '#FFFFFF'};
const FONT = 'Inter, Segoe UI, Arial, sans-serif';

const rise = (frame: number, fps: number, delay: number) => spring({frame: Math.max(0, frame - delay), fps, config: {damping: 20, stiffness: 100, mass: 0.8}});

const Card: React.FC<{label: string; value?: string; note?: string; accent: string; progress: number}> = ({label, value, note, accent, progress}) => (
  <div style={{flex: 1, minWidth: 0, height: 350, borderRadius: 22, border: `2px solid ${C.line}`, background: C.white,
    padding: '36px 42px', boxShadow: '0 18px 50px rgba(14,47,66,.07)', opacity: progress,
    transform: `translateY(${(1 - progress) * 30}px)`}}>
    <div style={{width: 66, height: 8, borderRadius: 8, background: accent, marginBottom: 30}} />
    <div style={{fontSize: 26, fontWeight: 700, color: C.muted, letterSpacing: 2, textTransform: 'uppercase'}}>{label}</div>
    <div style={{fontSize: value && value.length > 18 ? 44 : 64, fontWeight: 730, color: C.night, marginTop: 34, lineHeight: 1.08}}>{value || '—'}</div>
    <div style={{fontSize: 28, color: C.muted, marginTop: 30, lineHeight: 1.28}}>{note}</div>
  </div>
);

const Flow: React.FC<{visual: Visual; frame: number; fps: number}> = ({visual, frame, fps}) => {
  const labels = [visual.left_label || 'INPUT', visual.center_label || 'METHOD', visual.right_label || 'OUTPUT'];
  return <div style={{display: 'flex', alignItems: 'center', width: '100%', height: 360, gap: 25}}>
    {labels.map((label, i) => <React.Fragment key={i}>
      <div style={{flex: 1, height: i === 1 ? 300 : 235, borderRadius: 24,
        background: i === 1 ? C.night : C.white, color: i === 1 ? C.white : C.night,
        border: i === 1 ? 'none' : `2px solid ${C.line}`, boxShadow: '0 20px 55px rgba(14,47,66,.08)',
        display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 30,
        fontSize: 37, fontWeight: 700, letterSpacing: 1,
        opacity: rise(frame, fps, i * 12), transform: `translateY(${(1 - rise(frame, fps, i * 12)) * 40}px)`}}>{label}</div>
      {i < 2 && <div style={{width: 80, height: 4, background: C.teal, position: 'relative',
        opacity: rise(frame, fps, 18 + i * 12)}}>
        <div style={{position: 'absolute', right: -3, top: -8, borderTop: '10px solid transparent', borderBottom: '10px solid transparent', borderLeft: `18px solid ${C.teal}`}} />
      </div>}
    </React.Fragment>)}
  </div>;
};

const Media: React.FC<{asset: Asset}> = ({asset}) => {
  const src = staticFile(asset.path.replace(/^public[\\/]/, '').replaceAll('\\', '/'));
  const isVideo = /\.(mp4|mov|webm)$/i.test(asset.path);
  return <div style={{height: 430, width: '100%', overflow: 'hidden', borderRadius: 18, background: '#E5EEF0', position: 'relative'}}>
    {isVideo ? <OffthreadVideo src={src} muted style={{height: '100%', width: '100%', objectFit: 'contain'}} /> :
      <Img src={src} style={{height: '100%', width: '100%', objectFit: 'contain'}} />}
    <div style={{position: 'absolute', left: 20, top: 18, padding: '10px 17px', borderRadius: 6,
      background: C.night, color: C.white, fontSize: 20, fontWeight: 700, textTransform: 'uppercase'}}>{asset.kind.replace('-', ' ')}</div>
    <div style={{position: 'absolute', right: 20, bottom: 18, padding: '8px 12px', borderRadius: 6,
      background: 'rgba(255,255,255,.94)', color: C.navy, fontSize: 18}}>{asset.credit}</div>
  </div>;
};

const Scene: React.FC<{scene: SceneData}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const dark = scene.kind === 'title' || scene.kind === 'closing';
  const foreground = dark ? C.white : C.night;
  const first = rise(frame, fps, 0);
  const second = rise(frame, fps, 9);
  const asset = (film.assets as Asset[]).find(a => scene.asset_ids.includes(a.id));
  const visual = scene.visual || {};
  const isFlow = ['system', 'method', 'mechanism'].includes(scene.kind);
  const isPair = ['problem', 'comparison', 'result'].includes(scene.kind);

  return <AbsoluteFill style={{background: dark ? C.night : C.paper, color: foreground, fontFamily: FONT, overflow: 'hidden'}}>
    <div style={{position: 'absolute', width: 630, height: 630, border: `2px solid ${dark ? '#31556A' : '#DFE9EC'}`,
      borderRadius: '50%', right: -105, top: -230, transform: `scale(${0.94 + first * .08})`}} />
    <div style={{position: 'absolute', width: 390, height: 390, border: `2px solid ${dark ? '#31556A' : '#DFE9EC'}`,
      borderRadius: '50%', right: 20, top: -100}} />
    <div style={{position: 'absolute', width: 9, height: 900, left: 0, background: C.teal}} />
    <div style={{position: 'absolute', top: 67, left: 104, fontSize: 24, letterSpacing: 3, fontWeight: 760,
      color: dark ? '#8ED0D9' : C.teal, opacity: first}}>{scene.eyebrow}</div>
    <div style={{position: 'absolute', top: dark ? 168 : 132, left: 100, width: dark ? 1500 : 1690,
      fontSize: dark ? 94 : 70, lineHeight: 1.08, letterSpacing: -2.4, fontWeight: 750,
      opacity: first, transform: `translateY(${(1 - first) * 34}px)`}}>{scene.headline}</div>
    <div style={{position: 'absolute', top: dark ? 395 : 268, left: 104, width: 1550,
      fontSize: dark ? 40 : 32, lineHeight: 1.28, color: dark ? '#D2E3EB' : C.muted,
      opacity: second, transform: `translateY(${(1 - second) * 20}px)`}}>{scene.body}</div>
    {dark && <div style={{position: 'absolute', top: 620, left: 104, fontSize: 26, lineHeight: 1.4,
      color: '#AFCAD8', opacity: rise(frame, fps, 18)}}>
      {scene.kind === 'title' ? <>{film.paper.authors}<br />{film.paper.institution}</> : film.paper.title}
    </div>}
    {!dark && <div style={{position: 'absolute', top: 365, left: 104, right: 104}}>
      {asset && <Media asset={asset} />}
      {!asset && isFlow && <Flow visual={visual} frame={frame} fps={fps} />}
      {!asset && isPair && <div style={{display: 'flex', gap: 36, width: '100%', alignItems: 'center'}}>
        <Card label={visual.left_label || 'BASELINE'} value={visual.left_value} note={visual.left_note} accent={C.amber} progress={rise(frame, fps, 7)} />
        <div style={{fontSize: 58, color: C.teal, fontWeight: 600, opacity: rise(frame, fps, 22)}}>→</div>
        <Card label={visual.right_label || 'METHOD'} value={visual.right_value} note={visual.right_note} accent={C.teal} progress={rise(frame, fps, 20)} />
      </div>}
    </div>}
    <div style={{position: 'absolute', left: 104, right: 104, bottom: 88, height: 1, background: dark ? '#446171' : C.line}} />
    <div style={{position: 'absolute', left: 104, right: 104, bottom: 35, fontSize: 25,
      color: dark ? '#CEE0E8' : C.navy, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{scene.caption}</div>
    {film.settings.fixture && <div style={{position: 'absolute', top: 54, right: 76, color: dark ? '#BFD6DE' : C.muted,
      fontSize: 19, fontWeight: 750, letterSpacing: 1.2}}>SYNTHETIC FIXTURE · REPLACE BEFORE PUBLISHING</div>}
  </AbsoluteFill>;
};

export const PaperFilm: React.FC = () => {
  let cursor = 0;
  return <AbsoluteFill>{(film.scenes as SceneData[]).map(scene => {
    const from = cursor;
    const durationInFrames = Math.round(scene.seconds * film.settings.fps);
    cursor += durationInFrames;
    return <Sequence key={scene.id} from={from} durationInFrames={durationInFrames}><Scene scene={scene} /></Sequence>;
  })}</AbsoluteFill>;
};
