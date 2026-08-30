import {resolve} from 'node:path';
import {Config} from '@remotion/cli/config';

// Run Remotion from this project's 05-Remotion工程 directory. These exclusions
// only reduce Webpack file watching; they do not hide files from Git or grant
// permission to read another project or the shared motion library.
const remotionRoot = __dirname;
const currentProjectRoot = resolve(remotionRoot, '..');

Config.overrideWebpackConfig((currentConfiguration) => ({
  ...currentConfiguration,
  watchOptions: {
    ...currentConfiguration.watchOptions,
    ignored: [
      resolve(remotionRoot, 'node_modules/**'),
      resolve(remotionRoot, 'dist/**'),
      resolve(remotionRoot, 'build/**'),
      resolve(remotionRoot, 'out/**'),
      resolve(remotionRoot, 'renders/**'),
      resolve(remotionRoot, '.cache/**'),
      resolve(remotionRoot, '.parcel-cache/**'),
      resolve(remotionRoot, '.remotion/**'),
      resolve(currentProjectRoot, '01-原始素材/**'),
      resolve(currentProjectRoot, '02-转录与剪辑决策/转录缓存/**'),
      resolve(currentProjectRoot, '03-精剪输出/代理片段/**'),
      resolve(currentProjectRoot, '06-预览与审核/**'),
      resolve(currentProjectRoot, '07-成片/**'),
    ],
  },
}));
