import React from 'react';
import {Composition} from 'remotion';
import film from '../film.json';
import {PaperFilm} from './PaperFilm';

export const Root: React.FC = () => {
  const durationInFrames = film.scenes.reduce((sum, scene) => sum + Math.round(scene.seconds * film.settings.fps), 0);
  return <Composition
    id="PaperFilm"
    component={PaperFilm}
    durationInFrames={durationInFrames}
    fps={film.settings.fps}
    width={film.settings.width}
    height={film.settings.height}
  />;
};
