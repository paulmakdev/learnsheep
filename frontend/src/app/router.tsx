import { Routes, Route } from 'react-router-dom';
import Home from '../pages/Home';
import LessonPage from '../pages/Lesson';
import Unknown from '../pages/Unknown'
import { mapLesson } from '../routing-data/mapLesson';

function generateCurriculumRoutes() {
  const routes: React.ReactElement[] = [];

  for (const [moduleSlug, moduleData] of Object.entries(mapLesson)) {
    for (const [subjectSlug, subjectData] of Object.entries(moduleData.subjects)) {
      for (const lessonSlug of subjectData.lessons) {
        routes.push(
          <Route
            key={`${moduleSlug}-${subjectSlug}-${lessonSlug}`}
            path={`/${moduleSlug}/${subjectSlug}/${lessonSlug}`}
            element={<LessonPage />}
          />
        );
      }
    }
  }

  return routes;
}

export default function Router() {
  console.log(generateCurriculumRoutes())
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      {/* canonical */}
      <Route path="/lesson/:lessonSlug" element={<LessonPage />} />

      {/* hierarchical alias */}
      <Route
        path="/:moduleSlug/:subjectSlug/:lessonSlug"
        element={<LessonPage />}
      />
      <Route path="*" element={<Unknown />} />
    </Routes>
  );
}
