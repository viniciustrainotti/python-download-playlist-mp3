# Python Download Playlist MP3

Simple script to download Youtube videos to converter to mp3 files.

## Setup

Create a file CSV from playlist Spotify.

For example to file `all_songs.csv`. The tracklist was download for site [Spotlistr](https://www.spotlistr.com/export/spotify-playlist) from [Playlist Spotify](https://open.spotify.com/playlist/3TLElzScImUsLr8hykJmVH)

### Format CSV File
```txt
artista,musica
"NAME_ARTIST1; NAME_ARTIST2; NAME_ARTIST3","NAME_MUSIC"
"NAME_ARTIST1; NAME_ARTIST2;","NAME_MUSIC"
```

### Usage

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
# If filename another of all_songs.csv, change to script to support new name file.
python3 download.py
```