import {Composition} from 'remotion';
import {AsipMl, asipDuration} from './AsipMl';
export const RemotionRoot = () => (
  <Composition id="AsipMl" component={AsipMl} durationInFrames={asipDuration()} fps={30} width={1080} height={1920} />
);
