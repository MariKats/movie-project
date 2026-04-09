type Studio = {
  name: string;
  headquarters?: string;
}

export type Movie = {
  id: number;
  title: string;
  summary: string;
  year: number;
  poster: string;
  genres: string[];
  actors: string[];
  directors: string[];
  studio: Studio;
}