import yt_dlp
import sys
#this is actually horrible code god dayum >.<



def search_yt(query, max_results = 5):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True, #no download just get info
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        res = ydl.extract_info(f"ytsearch{max_results}:{query}", download = False)
        return res['entries']

def download_yt(url, path, name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': path + f"/{title if name == "" else name}.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



if(len(sys.argv) < 2):
    print('Usage: mus <link> <file name> <playlist>\n\nExample: mus https://www.youtube.com/watch?v=1a34aB5cD0 "Planeta Moldova - Am pula mare" "Muzica clasica" \n\nOr you can directly query yt and choose between the first results: \nmus <query> <file name> <playlist> <nr of results(default:5)>\n\nExample: mus "adrian norocel numai femei" "Adrian Norocel - Numai Femei" "muzica care e bn de ascultat" 8')
    sys.exit(0)

if("https://" in sys.argv[1]):
    path = "/home/toastu/Music" + f"{"" if len(sys.argv) < 4 else "/" + sys.argv[3]}"
    name = "" if len(sys.argv) < 3 else sys.argv[2]
    download_yt(sys.argv[1], path, name)
else:
    query = search_yt(sys.argv[1], max_results = 5 if len(sys.argv) < 5 else int(sys.argv[4]))
    print(f"Results for {sys.argv[1]}:\n")
    for i, video in enumerate(query, 1):
        print(f"{i}. {video['title']}")
        print(f"   URL: https://youtube.com/watch?v={video['id']}")
        print(f"   Duration: {video.get('duration', 'Unknown')} seconds\n")

    index = input(f"Which video to download (1-{len(query)}): ")

    download_yt(f"https://www.youtube.com/watch?v={query[int(index) - 1]['id']}", f"/home/toastu/Music/{"" if len(sys.argv) < 4 else sys.argv[3]}", f"{"" if len(sys.argv) < 3 else sys.argv[2]}")
        



  



