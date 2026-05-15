import { type ComponentType } from 'react';

const lessonModules = import.meta.glob<{ default: ComponentType }>(
  '/src/pages/lesson/*.tsx',
  { eager: true }
);

export const lessonMap: Record<string, ComponentType> = Object.fromEntries(
  Object.entries(lessonModules).map(([path, mod]) => {
    const slug = path.split('/').pop()!.replace('.tsx', '');
    return [slug, mod.default];
  })
);
