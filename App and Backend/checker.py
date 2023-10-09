import pandas as pd
from tensorflow import keras
import numpy as np
from sklearn.preprocessing import StandardScaler
import torch
import numpy as np
import pandas as pd
import librosa
import os
import sys
import sqlite3
from sqlite3 import Error
import warnings
import requests
import subprocess
from transformers import pipeline
import feedparser
import random

warnings.filterwarnings("ignore")


class utils:
    choosemicdevice = True
    dev = 0
    userid = 0
    label = 0
    cmd = 0

    def extract_features(self, files):
        # Sets the name to be the path to where the file is in my computer
        file_name = os.path.join((self.userid + "/" + str(files.file)))
        # Loads the audio file as a floating point time series and assigns the default sample rate
        # Sample rate is set to 22050 by default
        X, sample_rate = librosa.load(file_name, res_type="kaiser_fast")
        # Generate Mel-frequency cepstral coefficients (MFCCs) from a time series
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
        # Generates a Short-time Fourier transform (STFT) to use in the chroma_stft
        stft = np.abs(librosa.stft(X))
        # Computes a chromagram from a waveform or power spectrogram.
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        # Computes a mel-scaled spectrogram.
        mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
        # Computes spectral contrast
        contrast = np.mean(
            librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0
        )
        # Computes the tonal centroid features (tonnetz)
        tonnetz = np.mean(
            librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,
            axis=0,
        )
        # We add also the classes of each file as a label at the end
        label = files.label
        return mfccs, chroma, mel, contrast, tonnetz, [label]

    # def convertToFlac()


def get_weather_by_name(city_name):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": "b105573cd43e42f69e9130644231106", "q": city_name}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        location_name = weather_data["location"]["name"]
        region = weather_data["location"]["region"]
        country = weather_data["location"]["country"]
        condition = weather_data["current"]["condition"]["text"]
        temperature = weather_data["current"]["temp_c"]
        humidity = weather_data["current"]["humidity"]
        op = f"Weather in {location_name} is {temperature}°C with humidity of {humidity}%"
        return op
    else:
        print(f"Error: {response.status_code}")
        return None


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    conn = sqlite3.connect(db_file)

    return conn


def create_user(conn, user):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = """ INSERT INTO user(id,label,class)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()

    return cur.lastrowid


def querry(conn, qur):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(qur)

    rows = cur.fetchall()

    return rows


def convert_to_wav(file_path):
    file_path = os.path.abspath(file_path)
    file_name, file_extension = os.path.splitext(file_path)
    if file_extension.lower() != ".wav":
        wav_file = file_name + ".wav"
        output_file_path = os.path.join(os.path.dirname(file_path), wav_file)
        try:
            subprocess.run(["ffmpeg", "-y", "-i", file_path, output_file_path])
            print(f"File converted to WAV: {output_file_path}")
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting file: {e}")
        return wav_file
    else:
        print("File is already in WAV format.")
        return file_path


def stt(filename):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-base",
        chunk_length_s=30,
        device=device,
    )
    transcription = pipe(filename, batch_size=8)["text"]
    print(transcription)
    return transcription


def classify_text(text):
    classifier = pipeline(model="facebook/bart-large-mnli")

    # Perform text classification
    results = classifier(text, candidate_labels=["weather", "joke", "fact", "news"])

    # Retrieve the label with the highest score
    max_score_idx = max(
        range(len(results["scores"])), key=results["scores"].__getitem__
    )
    label = results["labels"][max_score_idx]
    score = results["scores"][max_score_idx]

    return label, score


def joke():
    url = "https://official-joke-api.appspot.com/jokes/programming/random"

    try:
        response = requests.get(url)
        data = response.json()
        joke = data[0]["setup"] + " " + data[0]["punchline"]
        return joke

    except Exception as e:
        print("Error occurred while fetching a joke:", str(e))
        return "Oops! Something went wrong."


def get_news_briefing():
    rss_url = "http://feeds.bbci.co.uk/news/rss.xml"

    try:
        feed = feedparser.parse(rss_url)

        articles = []
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            description = entry.description
            published_date = entry.published

            article = {
                "title": title,
                "link": link,
                "description": description,
                "published_date": published_date,
            }

            articles.append(article)

        return articles[random.randint(0, len(article))]["title"]

    except Exception as e:
        print("Error occurred while fetching news:", str(e))
        return []


def fact():
    url = "https://useless-facts.sameerkumar.website/api"

    try:
        response = requests.get(url)
        data = response.json()

        return data["data"]

    except Exception as e:
        print("Error occurred while fetching a fact:", str(e))
        return "Oops! Something went wrong."


database = "./user.db"


def identification(uid, label):
    print("Checking")
    util = utils()
    util.userid = uid
    util.label = label
    files = os.listdir(util.userid + "/")
    data = pd.DataFrame(files)
    data = data.rename(columns={0: "file"})
    data = data[data["file"].str.contains("cmd")]
    data["label"] = util.label
    model = keras.models.load_model("spktvrfiwithlabel")
    features_label = data.apply(util.extract_features, axis=1)
    index = data.index[data["file"].str.contains("cmd")].tolist()[0]
    features = []
    features.append(
        np.concatenate(
            (
                features_label[index][0],
                features_label[index][1],
                features_label[index][2],
                features_label[index][3],
                features_label[index][4],
                features_label[index][5],
            ),
            axis=0,
        )
    )
    X = np.array(features)
    # from joblib import load

    # ss = load("std_scaler.bin")
    # X_train = ss.transform(X)
    predict_x = model.predict(X)
    preds = np.argmax(predict_x, axis=1)
    predClass = np.bincount(preds).argmax()
    print("Pridicted Class", predClass)
    conn = create_connection(database)
    result = querry(conn, f"select * from user where id='{uid}'")[0]
    if int(result[2]) == int(predClass.item()):
        newfile = convert_to_wav(uid + "/" + str(data["file"][index]))
        text = stt(newfile)
        label = classify_text(text)
        op = ""
        if label[0] == "weather":
            print("Fetching Weather")
            op = get_weather_by_name("Srinagar")
        elif label[0] == "joke":
            print("Fetching Joke")
            op = joke()
        elif label[0] == "fact":
            print("Fetching fact")
            op = fact()
        elif label[0] == "news":
            op = get_news_briefing()

        return True, op
    else:
        return (
            False,
            "You are not authorized to give any commands on behalf of this user",
        )


if __name__ == "__main__":
    identification(sys.argv[1], sys.argv[2])
