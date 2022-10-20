import requests, time, json
from key_config import API_KEY_ASSEMBLYAI
from datetime import datetime

# upload to assemblyai
headers = {'authorization': API_KEY_ASSEMBLYAI}  # used for authentication
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

def upload(filename):
    def read_file(filename, chunk_size=5242880):   # reading data file
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint,   # when uploading a file to assemblyai doing a post request so need endpoint, API key, and file to transcribe
                            headers=headers,
                            data=read_file(filename))

    #print(upload_response.json())
    audio_url = upload_response.json()['upload_url']
    return audio_url

# transcribe
def transcribe(audio_url, sentiment_analysis):
    transcript_request = { 
        'audio_url': audio_url,  # url response from assemblyai in the upload
        'sentiment_analysis': sentiment_analysis
    }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)  # 
    #print(transcript_response.json())
    job_id = transcript_response.json()['id']
    return job_id

#audio_url = upload(filename)
# transcript_id = transcribe(audio_url)
#print(transcript_id)


# poll to see when transcription done
# Send get request instead of post. Use polling endpoint. Not sending any data so just need endpoint and headers. Just asking for status.
# When sending data to API use post request. If only getting information/status use the get request.
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    #print(polling_response.json())
    return polling_response.json()

def get_transcription_result_url(audio_url, sentiment_analysis):
    transcript_id = transcribe(audio_url, sentiment_analysis)
    while True:
        data = poll(transcript_id)  # seen in response as polling_response.json()['status']
        if data['status'] == 'completed':  
            return data, None
        elif data['status'] == 'error':
            return data, data["error"]
        print('Waiting 30 seconds')
        time.sleep(30)

# Save transcription. Notice went from from 'filename' to 'title' for file naming
def save_transcript(audio_url, title, sentiment_analysis=False):
    print("{0} Audio file uploaded. Waiting for transcription to complete".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    data, error = get_transcription_result_url(audio_url, sentiment_analysis)
    if data:
        filename = title + ".txt"
        with open(filename, "w") as f:
            f.write(data['text'])
        if sentiment_analysis:
            filename = title + "_sentiments.json"
            with open(filename, "w") as f:
                sentiments = data["sentiment_analysis_results"] # can get key "sentiment_analysis_results" from assemblyai docs
                json.dump(sentiments, f, indent=4)  # dump into file "f" and indent for readability
        print("{0} Transcription saved".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    elif error:
        print("Error on transcript", error)