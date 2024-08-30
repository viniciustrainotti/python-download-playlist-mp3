import pandas as pd
from pytube import YouTube
from pydub import AudioSegment
import os
import requests
from urllib.parse import quote_plus
from io import BytesIO
from pytube import cipher
import re

def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
        # https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
        # var Bpa = [iha];
        # ...
        # a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
        # Bpa.length || iha("")) }};
        # In the above case, `iha` is the relevant function name
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    #logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            #logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )

cipher.get_throttling_function_name = get_throttling_function_name


def search_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    response = requests.get(search_url)
    video_id_start = response.text.find('watch?v=')
    
    if video_id_start == -1:
        print(f"Vídeo não encontrado para: {query}")
        return None
    
    video_id = response.text[video_id_start + len('watch?v='):video_id_start + len('watch?v=') + 11]
    return f"https://www.youtube.com/watch?v={video_id}"

def download_video_as_mp3(youtube_url, artist, title):
    yt = YouTube(youtube_url)
    print(yt.title)
    stream = yt.streams.filter(only_audio=True).first()
    print(f"Baixando {artist} - {title}...")

    # Baixar o áudio em formato MP4
    output_file = stream.download(filename=f"{artist} - {title}.mp4")

    # Convertendo para MP3 usando pydub
    mp3_file = f"{artist} - {title}.mp3"
    AudioSegment.from_file(output_file).export(mp3_file, format="mp3")

    # Remover o arquivo MP4 original
    os.remove(output_file)
    print(f"{artist} - {title} baixado e convertido para MP3 com sucesso.")

def download_songs_from_csv(csv_file):
    df = pd.read_csv(csv_file, delimiter=',', quotechar='"')
    for index, row in df.iterrows():
        artist = row['artista'].strip()
        title = row['musica'].strip()
        search_query = f"{artist} {title}"
        youtube_url = search_youtube(search_query)
        print("URL")
        print(youtube_url)
        
        if youtube_url:
            download_video_as_mp3(youtube_url, artist, title)

if __name__ == "__main__":
    csv_file = "restante.csv"  # Nome do arquivo CSV
    download_songs_from_csv(csv_file)
