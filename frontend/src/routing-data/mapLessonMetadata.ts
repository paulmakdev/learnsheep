export type LessonMetadataProps = {
  title: string;
  full_title?: string;
  description: string;
  sub_title?: string;
  definitions?: Record<string, string>;
};

export const mapLessonMetadata: Record<string, LessonMetadataProps> = {
  "addition": {
    title: "Addition",
    description: "Learn to count and add things together"
  },
  "subtraction": {
    title: "Subtraction",
    description: "Learn to subtract and take away from numbers"
  },
  "multiplication": {
    title: "Multiplication",
    description: "Learn to add repeatedly, also known as multiplication "
  },
  "division": {
    title: "Division",
    description: "Learn to divide into pieces"
  },
  "operation-practice": {
    title: "Operation Practice",
    description: "Practice addition, subtraction, multiplication, and division in one lesson."
  },
  "order-of-operations": {
    title: "Order of Operations",
    description: "Learn the order of addition/subtraction, multiplication/divison, and parentheses/exponents",
  },
  "exponents-and-roots": {
    title: "Exponents and Roots",
    description: "Learn about multiplication shorthand (exponents) and roots.",
  },
  "variables": {
    title: "Variables",
    description: "Learn about putting values into boxes (variables), and how to use them"
  },
  "functions": {
    title: "Functions",
    description: "Learn about set series of steps, aka functions"
  },
  "recursion": {
    title: "Recursion",
    full_title: "Recursion and Recursive Functions",
    sub_title: "Loops? Nah, just go down into the function and come back up",
    description: "Learn about recursive functions that use themselves for repeating processes",
  },
  "nouns": {
    title: "Nouns",
    description: "People, places, and things.",
    definitions: {
       "Noun": "Person, place, thing, or idea",
       "Proper noun": "Starts with a capital letter and uses a specific name. I.e. Learnsheep, Mr. John",
       "Common noun": "Starts with a lowercase letter and does not use a specific name. I.e. website, rock",
       "Concrete noun": "Something that you can touch or see.",
       "Abstract noun": "Something you can think or feel.",
       "Countable noun": "Something you can count. Like rocks",
       "Uncountable noun": "Something you cannot directly count."
    },

  },
  "pronouns": {
    title: "Pronouns",
    description: "Nouns that represent other nouns"
  },
  "adjectives": {
    title: "Adjectives",
    description: "Words that describe nouns"
  },
  "verbs": {
    title: "Verbs",
    description: "Words that show action"
  },
  "adverbs": {
    title: "Adverbs",
    description: "Words that describe verbs"
  },
  "prepositions": {
    title: "Prepositions",
    description: "Words that help you express relations between words"
  },
  "subject-verb-agreement": {
    title: "Subject-Verb Agreement",
    description: "All nouns that do things must "
  },
  "possessives": {
    title: "Possessives",
    description: "Words that show belonging"
  },
  "direct-objects": {
    title: "Direct Objects",
    description: "Things that you do things to"
  },
  "indirect-objects": {
    title: "Indirect Objects",
    description: "Things that are part of an action, but the action isn't done to them"
  },
  "clauses-and-phrases": {
    title: "Clauses and Phrases",
    description: "How to form sentences, express related ideas, and prevent run-on sentences"
  },
  "object-of-the-preposition": {
    title: "Object of the Preposition",
    description: "Used by prepositions to help them express relations between words"
  },
  "gerunds-and-participles": {
    title: "Gerunds and Participles",
    description: "Phrases that act like verbs or adjectives, but aren't"
  },
  "ending-punctuation": {
    title: "Ending Punctuation",
    description: "How to end sentences based on the meaning of the sentence"
  },
  "commas": {
    title: "Commas",
    description: "Every reason you would need to use a comma."
  },
  "sentence-breaking-punctuation": {
    title: "Sentence-Breaking Punctuation",
    description: "When to use punctuation between phrases, and which punctuation to use"
  },
  "ultimate-grammar-practice": {
    title: "Ultimate Grammar Practice",
    description: "The best practice you will ever have. Explains wrong and right answers"
  }
};
