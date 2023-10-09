import * as React from "react";
import { Text, View, StyleSheet,Platform } from "react-native";
import { Button } from "../components/button";
import { Audio } from "expo-av";
import * as FileSystem from "expo-file-system";
import {FLASK_BACKEND} from "./consts";
import uuid from 'react-native-uuid';
import TopBarComponent from '../components/topbar';
import  ScrollableTextBox from "../components/results"


export default function Recorder({ route, navigation }) {
  const{cmd,id}=route.params;
  const [recording, setRecording] = React.useState();
  const [text, setText] = React.useState("");
  const[show,setShow]=React.useState(false);
  const[msg,setMsg]=React.useState(true);
  const[uid,setUuid]=React.useState(id);
  const [output, setOutput] = React.useState("");
  const [count, setCount] = React.useState(0);
  if(uid==-1)
  {
    setUuid(uuid.v4().slice(0,4))
  }
  // const [word, setWord] = React.useState("");
  const text_lines = [
    "Hello",
    "Can you please repeat",
    "What is your favorite color",
    "Could you introduce yourself",
    "Please describe your most memorable vacation",
    "Would you mind reading this passage",
    "Can you sing a few lines from your favorite song", 
    "Tell me a joke that always makes you laugh",
    "What is your opinion on artificial intelligence",
    "Could you recite a famous quote or poem",
  ];
  
  async function startRecording() {
    if(cmd==true)
      {
        setCount(-1);
      }
    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });
      const { recording } = await Audio.Recording.createAsync({
        android: {
          extension: ".mp4",
          audioEncoder: Audio.RECORDING_OPTION_ANDROID_AUDIO_ENCODER_AAC,
          outputFormat: Audio.RECORDING_OPTION_ANDROID_OUTPUT_FORMAT_MPEG_4,
        },
        ios: {
          extension: ".wav",
          sampleRate: 44100,
          numberOfChannels: 2,
          bitRate: 128000,
          audioQuality: Audio.RECORDING_OPTION_IOS_AUDIO_QUALITY_HIGH,
          outputFormat: Audio.RECORDING_OPTION_IOS_OUTPUT_FORMAT_LINEARPCM,
        },
      });
      setRecording(recording);
    } catch (err) {
      console.error("Failed to start recording", err);
    }
  }

  async function stopRecording() {
    setRecording(undefined);
    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();

    try {
      const response = await FileSystem.uploadAsync(
        FLASK_BACKEND()+"/audio",
        uri,{
          fieldName: 'Audio',
          httpMethod: "POST",
          headers: {
              new:JSON.stringify({'p':Platform.OS,'uid':uid,'tno':count+1}),
          }
        }
      );
      console.log(count)
      const body = JSON.parse(response.body);
      if(body.col=="red")
      {
          setMsg(false);
          setText(body.text);
          setShow(true);
          setTimeout(() => {setShow(false);setMsg(true);}, 3000);

      }
      else{
        setText(body.text);
        setShow(true);
        setMsg(true);
        setTimeout(() => {setShow(false);}, 3000);
      }
      if(cmd==true)
      {
        if(body.output.length>=0)
        {
          setOutput(body.output)
        }
      }
      if(cmd!=true)
      {
        setCount(count+1);
        console.log(count);
        if(count>=9)
        {
          setCount(-1);
          // console.log('Cmd Called');
          navigation.navigate('Recorder',{cmd:true,id:uid})
        }
      }
      
    } catch (err) {
      console.error(err);
      setMsg(false);
    }
  }
  
  return (
    <View style={styles.container}>
      <TopBarComponent title={uid} />
      <ScrollableTextBox data={cmd==true&&output} />
      <View style={{height:250}}>
      <Text style={{
    fontSize: 16,
    fontWeight: 'bold',
    letterSpacing: 0.25,
    color: 'black',
    textAlign:'center',
    marginVertical:10,
    paddingBottom:10,

  }}>{cmd==true ?"Please Give Your Command":"Please speak the line given below"}</Text>
      {cmd!=true&&<Text style={styles.text}>{text_lines[count]}</Text>}
      <Button
        title={recording ? "Stop Recording" : "Start Recording"}
        onPress={recording ? stopRecording : startRecording}
      />
      { show && 
    <Text style={{
      marginTop:5,
      borderWidth:1,
      borderBottomColor:msg==true?'green':'red',
      textAlign:'center',
      color:msg==true?'green':'red',
      fontWeight: 'bold',
    }}>{text}</Text>}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: 'stretch',
    paddingHorizontal:50,
    justifyContent: 'space-between',
  },text: {
    fontSize: 16,
    lineHeight: 21,
    fontWeight: 'bold',
    letterSpacing: 0.25,
    color: 'black',
    textAlign:'center',
    marginVertical:10,
    paddingVertical:10,
    borderColor:'blue',
    borderWidth:1,
  },
});