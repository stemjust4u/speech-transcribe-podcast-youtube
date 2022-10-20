# https://github.com/ytdl-org/youtube-dl

import youtube_dl

ydl = youtube_dl.YoutubeDL() # setup an instance

def get_video_infos(url):  
    with ydl:         # ydl object context manager
        result = ydl.extract_info(
            url,
            download=False  # do not need to download since just passing url to assemblyai
        )
    if "entries" in result:  # if entries key is in result then means there is a playlist
        return result["entries"][0]  # return the first video of the playlist
    return result

def get_audio_url(video_info):
    # print(video_info)
    for f in video_info["formats"]:  # iterate over info
        # print(f["ext"]) # print extensions
        if f["ext"] == "m4a":
            return f["url"]


if __name__ == "__main__":
    video_info = get_video_infos("https://www.youtube.com/watch?v=e-kSGNzu0hM")
    audio_url = get_audio_url(video_info)
    print(audio_url)
