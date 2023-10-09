class utils:
    def extract_features(files):
        import os
        import librosa
        import numpy as np
        # Sets the name to be the path to where the file is in my computer
        file_name = os.path.join(os.path.abspath('LibriSpeech/voice')+'/'+str(files.file))
        # Loads the audio file as a floating point time series and assigns the default sample rate
        # Sample rate is set to 22050 by default
        X, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
        # Generate Mel-frequency cepstral coefficients (MFCCs) from a time series 
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
        # Generates a Short-time Fourier transform (STFT) to use in the chroma_stft
        stft = np.abs(librosa.stft(X))
        # Computes a chromagram from a waveform or power spectrogram.
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
        # Computes a mel-scaled spectrogram.
        mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)
        # Computes spectral contrast
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
        # Computes the tonal centroid features (tonnetz)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X),
        sr=sample_rate).T,axis=0)
        # We add also the classes of each file as a label at the end
        # label = files.label
        return mfccs, chroma, mel, contrast, tonnetz
    
    def recordAudio(self,filename,duration):
        import sounddevice as sd
        from scipy.io.wavfile import write

        fs = 48000  # Sample rate
        seconds = duration # Duration of recording

        print(":---Input Devices available---:")
        print(sd.query_devices())
        dev=int(input("Select the device:"))
        print(":---Input Device Selected---:")
        sd.default.device=sd.query_devices()[dev]['name']
        print(sd.default.device)
        print("Recording")
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        print(f"Saving it as {filename}")
        write(filename, fs, myrecording)
    
    def getVoiceSamples(self):
        import os
        import librosa
        import numpy as np
        import uuid
        text_lines = {
        "Hello": 2.5,
        "Can you please repeat": 4.2,
        "What is your favorite color": 5.1,
        "Could you introduce yourself": 6.3,
        "Please describe your most memorable vacation": 7.8,
        "Would you mind reading this passage": 9.2,
        "Can you sing a few lines from your favorite song": 11.5,
        "Tell me a joke that always makes you laugh": 4.7,
        "What is your opinion on artificial intelligence": 6.8,
        "Could you recite a famous quote or poem": 8.1
        }
        print('Repeat the lines given below to generate your voice sample')
        speakerid=uuid.uuid1().hex[:10]
        lineCount=0
        os.mkdir(speakerid)
        for line in text_lines:
            print(line)
            lineCount+=1
            utils.recordAudio(speakerid+"/"+str(lineCount)+'.wav',10)
