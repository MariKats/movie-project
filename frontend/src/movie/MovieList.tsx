import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import ListSubheader from '@mui/material/ListSubheader';
import type { Movie } from './models';
import IconButton from '@mui/material/IconButton';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import './MovieList.css';

interface MovieListProps {  
  movies: Movie[];
}

export default function MovieList({ movies }: MovieListProps) {
  const theme = useTheme();
  const isXs = useMediaQuery(theme.breakpoints.down('sm'));  // < 600px
  const isSm = useMediaQuery(theme.breakpoints.down('md')); // < 900px

  const cols = isXs ? 1 : isSm ? 2 : 3;

  const handleItemClick = (title: string) => {
    alert(`Clicked on ${title}`);
  };
  
  const listToText = (arr?: string[]) => (arr?.length ? arr.join(', ') : 'N/A');

  return (
    <div className="movie-list-container">
      <ImageList className="movie-list" cols={cols} gap={8}>
        <ImageListItem key="Subheader" cols={cols} style={{ height: 'auto' }}>
          <ListSubheader component="div">Movies</ListSubheader>
        </ImageListItem>

        {movies.map((item) => (
          <ImageListItem 
            key={item.id} 
            onClick={() => handleItemClick(item.title)} 
            className='movie-item'
          >
            <img
              className="movie-image"
              srcSet={`${item.poster}?w=248&fit=crop&auto=format&dpr=2 2x`}
              src={`${item.poster}?w=248&fit=crop&auto=format`}
              alt={item.title}
              loading="lazy"
            />
            <div className="hover-deadzone" aria-hidden="true" />
            
            <Box className="hover-info">
              <div className="hover-header">
                <Typography variant="subtitle2" className="hover-title">
                  {item.title}
                </Typography>
                <Typography variant="caption" className="hover-year">
                  {item.year}
                </Typography>
              </div>

              <Typography variant="caption" className="hover-summary">
                {item.summary || 'No summary available.'}
              </Typography>

              <div className="hover-meta-row">
                <span className="meta-label">Genres</span>
                <span className="meta-value">{listToText(item.genres)}</span>
              </div>
              <div className="hover-meta-row">
                <span className="meta-label">Actors</span>
                <span className="meta-value">{listToText(item.actors)}</span>
              </div>
              <div className="hover-meta-row">
                <span className="meta-label">Directors</span>
                <span className="meta-value">{listToText(item.directors)}</span>
              </div>
            </Box>

            <ImageListItemBar
              className='movie-item-bar'
              title={`${item.title}`}
              subtitle={`${item.year}`}
              style={{ textAlign: 'left' }}
              position='top'
              actionIcon={
                  <IconButton sx={{ color: 'white' }} aria-label={`star ${item.title}`}>
                    <StarBorderIcon />
                  </IconButton>
                }
                actionPosition="left"
            />
          </ImageListItem>
        ))}
      </ImageList>
    </div>
  );
}

