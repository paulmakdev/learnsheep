import { useParams } from 'react-router-dom';
import { resolveLesson } from '../utils/resolveLesson';

interface LessonContext {
  lessonSlug: string;
  canonicalUrl: string;
}

export function prepareLessonUrl(): LessonContext {
  const { lessonSlug, moduleSlug, subjectSlug } = useParams<{
    lessonSlug?: string;
    moduleSlug?: string;
    subjectSlug?: string;
  }>();

  if (!lessonSlug) {
    throw new Error('lessonSlug missing');
  }

  // If coming from hierarchical route, validate it
  const resolved =
    moduleSlug && subjectSlug
      ? resolveLesson(moduleSlug, subjectSlug, lessonSlug)
      : lessonSlug;

  if (!resolved) {
    console.log(moduleSlug)
    console.log(subjectSlug)
    console.log(lessonSlug)
    return {lessonSlug: "not-found", canonicalUrl: "not-found"}
    throw new Error('Invalid lesson route');
  }

  return {
    lessonSlug: resolved,
    canonicalUrl: `https://learnsheep.com/lesson/${resolved}`,
  };
}
