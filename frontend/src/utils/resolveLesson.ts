// utils/resolveLesson.ts
import { mapLesson } from '../routing-data/mapLesson';

export function resolveLesson(
  moduleSlug: string,
  subjectSlug: string,
  lessonSlug: string
): string | null {
  console.log("resolving")
  console.log(moduleSlug)
  const module = mapLesson[moduleSlug];
  if (!module) return null;
  console.log("module exists")

  const subject = module.subjects[subjectSlug];
  if (!subject) return null;
  console.log("subject exists")

  if (!subject.lessons.includes(lessonSlug)) return null;

  console.log("made it here?")

  return lessonSlug;
}
