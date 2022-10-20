# to see origin of code https://www.assemblyai.com/docs/audio-intelligence#sentiment-analysis

import json
from yt_extractor import get_audio_url, get_video_infos
from api_communication import save_transcript

def save_video_sentiments(url):
    video_infos = get_video_infos(url)
    audio_url = get_audio_url(video_infos)
    title = video_infos["title"]    # title will be filename. get it from video key "title"
    title = title.strip().replace(" ", "_") # get rid of beg/end spaces and then replace middle spaces with _
    title = "data/" + title   # will store in data folder
    save_transcript(audio_url, title, sentiment_analysis=True)

if __name__ == "__main__":
    # save_video_sentiments("https://www.youtube.com/watch?v=e-kSGNzu0hM")
    # once info is downloaded can comment out "save video sentiments" and work on the results file that was downloaded in data/
    with open("data/iPhone_13_Review:_Pros_and_Cons_sentiments.json", "r") as f:
        data = json.load(f)
    # read sentiment file and put in json object
    positives = [] # create lists for each category
    negatives = []
    neutrals = []
    for result in data:  # iterate over the json data
        text = result["text"]  # extract the 'text' info
        if result["sentiment"] == "POSITIVE":  # depending on which 'sentiment' append the 'text' to the corresponding list with append
            positives.append(text)
        if result["sentiment"] == "NEGATIVE":
            negatives.append(text)
        else:
            neutrals.append(text)

    n_pos = len(positives) # get length of the lists
    n_neg = len(negatives)
    n_neut = len(neutrals)

    print("Num positives:", n_pos)
    print("Num negatives:", n_neg)
    print("Num neutrals:", n_neut)

    r = n_pos / (n_pos + n_neg) # ignoring neutrals
    print(f"Positive ratio: {r:.3f}")