import './App.css'
import MovieList from './movie/MovieList';
import { movieData } from './movie/mock-data';

function App() {
  return <>
    <MovieList movies={movieData}/>
  </>;
}

export default App
