# Project Report of Pranav Singh Sambyal (2019BITE016) and Abijit Singh(2019BITE007)

## Model Buidling and Testing
- This contains the the file used to underand data and then form a model for the same.
- The file SpeakerVerificationTraining.ipynb is the main file which contains all information on model and its training with commants at places.
- It also contains 5 pretrained saved models:
  - spktvrfi & spktvrfidev is the model trained on main and dev dataset respectively with label(gender info) included.
  - spktvrfinolabel & spktvrfinolabeldev is the model trained on main and dev dataset respectively without label(gender info) information.
  - spktvrfiwithlabel is a varition of first 2 with changed activation functions

## App and Backend
- This contains the react native app 
- backend.py is the main backend file with get everything running

# Notes 
- Data set used is LibriSpeach and can be found [Here](https://www.openslr.org/12)
- For further information contact singhsambyalpranav@gmail.com
