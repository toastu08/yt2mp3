import yt_dlp


class Media_engine:
    def __init__(self, download_path):
        self.download_path = download_path
        #we keep track of the last query in a list idk may be useful
        self.result = []


    def clear_results(self):
        self.result.clear()

    def search_yt(self, query, max_results = 5):
        self.clear_results()
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True, 
        }

        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result_query = ydl.extract_info(f"ytsearch{max_results}:{query}", download = False)

            #filtering out just what the app needs from the dict
            self.result = [{k: res[k] for k in ['url', 'title','channel', 'thumbnails']} for res in result_query['entries']]
        return self.result

    

    def download(self, song = 0):
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': self.download_path + f"{self.result[song]["title"]}.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }

        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(self.result[song]["url"])

            
    
    def search_sc(self, query, max_results = 5):
        self.clear_results()

        ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'extract_flat': True, 
        }

        search_query = f"scsearch{max_results}:{query}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result_query = ydl.extract_info(search_query, download=False)
        
            self.result = [{k: res[k] for k in ['url', 'title', 'thumbnails']} for res in result_query['entries']]
        
        return self.result
    
            

#for testing
if __name__ == "__main__":

    #res = search_yt("shiawase vip")

    #print("select song:\n")
    #for i, song in enumerate(res):
    #    print(f"{i}. {song["title"]}\n")


    #path = "~/Music/"
    #selection = int(input())

    #download_yt(res[selection], path)

    me = Media_engine("~/Music/")

    result = me.search_sc("shiawase vip")

    for i in result:
        print(i)
        print('\n')
        

    #me.download_yt()




