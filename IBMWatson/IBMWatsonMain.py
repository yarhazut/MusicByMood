import json
from pathlib import Path
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='0nW4OX6Qlfv1I_6oRpepMpvi_eUpnh3_qBU19Glxxi-B',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
)
def createPostingIBM(songName,artist,text):
    try:
        data_folder = Path("C:\songs_after_post_LIWC")
        file_to_open = data_folder / "Songs_Watson.txt"
        jsonDump=getIBMVectorFromText(text)
        jsonDump['songName']=songName
        jsonDump['artist']= artist
        toPrint=json.dumps(jsonDump)
        print(toPrint)
        with open(file_to_open, 'a') as outfile:
            json.dump(toPrint, outfile)
            outfile.write('\n')
    except Exception:
        pass
def getIBMVectorFromText(text):
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(emotion=EmotionOptions()), language='english').get_result()
    jsonDump = response['emotion']['document']['emotion']
    return jsonDump