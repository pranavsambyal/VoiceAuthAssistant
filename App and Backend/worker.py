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
from joblib import load


# from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer,pipeline
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


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

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


database = "./user.db"


def main(uid, label):
    print("learning")
    util = utils()
    util.userid = uid
    util.label = 1
    files = os.listdir(util.userid + "/")
    data = pd.DataFrame(files)
    data = data.rename(columns={0: "file"})
    data["label"] = util.label
    model = keras.models.load_model("spktvrfiwithlabel")
    features_label = data.apply(util.extract_features, axis=1)
    features = []

    for i in range(0, len(features_label)):
        features.append(
            np.concatenate(
                (
                    features_label[i][0],
                    features_label[i][1],
                    features_label[i][2],
                    features_label[i][3],
                    features_label[i][4],
                    features_label[i][5],
                ),
                axis=0,
            )
        )
    X = np.array(features)
    # ss = load("std_scaler.bin")
    # X_train = ss.transform(X)
    predict_x = model.predict(X)
    preds = np.argmax(predict_x, axis=1)
    authoriseduserid = np.bincount(preds).argmax()
    conn = create_connection(database)
    print(authoriseduserid)
    with conn:
        values = (uid, label, int(authoriseduserid.item()))
        print(create_user(conn, values))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
