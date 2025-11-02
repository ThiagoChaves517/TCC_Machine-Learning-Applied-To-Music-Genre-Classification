# This script was made with Gemini 2.5 Pro, accessible by this link: https://gemini.google.com/share/46771f3bac3b

import os
import shutil
import pandas as pd

# Path to the FMA metadata and audio files
METADATA_DIR = 'fma_metadata'  # Folder which has the tracks.csv file (248.4 MB), which lists all the FMA Dataset tracks into columns. The track files in the chosen AUDIO_DIR will be rearrenged according to their genres in tracks.csv
AUDIO_DIR = 'fma_datasets/fma_small'       # Select the desired dataset of tracks from FMA. They may be: fma_small | fma_medium | fma_large | fma_full

def load_tracks(filepath):
    """Loads the tracks metadata from a CSV file."""
    tracks = pd.read_csv(filepath, index_col=0, header=[0, 1])
    # Convert columns with lists to actual lists
    columns_to_convert = [('track', 'genres'), ('track', 'genres_all')]
    for column in columns_to_convert:
        if column in tracks.columns:
            tracks[column] = tracks[column].apply(eval)
    return tracks

def reorganize_audio_by_genre(audio_dir, tracks_df):
    """
    Reorganizes audio files into folders named by their top-level genre.
    """
    # Create a new directory for the genre-sorted audio files
    output_dir = os.path.join(os.path.dirname(audio_dir), 'fma_small_genres')  # Name of the new folder with rearrenged tracks.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get a list of all audio files
    audio_files = []
    for root, _, files in os.walk(audio_dir):
        for file in files:
            if file.endswith('.mp3'):
                audio_files.append(os.path.join(root, file))

    for audio_file_path in audio_files:
        try:
            # Extract track ID from the filename
            track_id = int(os.path.basename(audio_file_path).split('.')[0])

            # Get the top-level genre for the track
            genre = tracks_df.loc[track_id, ('track', 'genre_top')]

            if pd.notna(genre):
                # Create a directory for the genre if it doesn't exist
                genre_dir = os.path.join(output_dir, genre)
                if not os.path.exists(genre_dir):
                    os.makedirs(genre_dir)

                # Move the audio file to the genre directory
                shutil.move(audio_file_path, os.path.join(genre_dir, os.path.basename(audio_file_path)))
                print(f"Moved {os.path.basename(audio_file_path)} to {genre}")
            else:
                print(f"Skipping {os.path.basename(audio_file_path)} - No top-level genre found.")

        except KeyError:
            print(f"Skipping {os.path.basename(audio_file_path)} - Track ID not found in metadata.")
        except Exception as e:
            print(f"An error occurred with file {os.path.basename(audio_file_path)}: {e}")

if __name__ == '__main__':
    tracks_filepath = os.path.join(METADATA_DIR, 'tracks.csv')
    if not os.path.exists(tracks_filepath):
        print(f"Error: The file {tracks_filepath} was not found.")
    elif not os.path.exists(AUDIO_DIR):
         print(f"Error: The directory {AUDIO_DIR} was not found.")
    else:
        # Load the tracks metadata
        tracks = load_tracks(tracks_filepath)
        # Reorganize the audio files
        reorganize_audio_by_genre(AUDIO_DIR, tracks)