export interface LessonConfig {
  lessons: string[];
}

export interface SubjectConfig {
  label: string;
  subjects: Record<string, LessonConfig & { label: string }>;
  image: string;
}

export const mapLesson: Record<string, SubjectConfig> = {
  math: {
    label: "Math",
    image: "/math_module.svg",
    subjects: {
      "pre-algebra": {
        label: "Pre-Algebra",
        lessons: [
                  "addition",
                  "subtraction",
                  "multiplication",
                  "division",
                  "operation-practice"
                ]
      },
      algebra: {
        label: "Algebra",
        lessons: [
                    "order-of-operations",
                    "exponents-and-roots",
                    "variables",
                  ]
      },
    },
  },
  "computer-science": {
    label: "Computer Science",
    image: '/computer_science_module.svg',
    subjects: {
      "principles": {
        label: "Principles",
        lessons: ["recursion", "variables"],
      },
    },
  },
  "grammar": {
    label: "Grammar",
    image: '/grammar_module.svg',
    subjects: {
      "parts-of-speech": {
        label: "Parts of Speech",
        lessons: ["nouns",
                  "pronouns",
                  "adjectives",
                  "verbs",
                  "adverbs",
                  "prepositions"
                ]
      },
      "syntax": {
        label: "Syntax",
        lessons: [
          "subject-verb-agreement",
          "possessives",
          "direct-objects",
          "indirect-objects",
          "clauses-and-phrases",
          "object-of-the-preposition",
          "gerunds-and-participles",
        ]
      },
      "punctuation": {
        label: "Punctuation",
        lessons: [
          "ending-punctuation",
          "commas",
          "sentence-breaking-punctuation",
        ]
      },
      "ultimate-grammar-practice": {
        label: "Ultimate Grammar Practice",
        lessons: [
          "ultimate-grammar-practice"
        ]
      }
    }
  }
};
