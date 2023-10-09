import { StyleSheet, Text, View,TextInput} from 'react-native'
import React from 'react'
import { Button } from '../components/button';
import {FLASK_BACKEND} from './consts';


export default function Login({ navigation}) {
  const [text,setText] = React.useState('');
  const [background, setBackgroundColor] = React.useState('');
  const onBth= async()=>{
    const res=await fetch(FLASK_BACKEND()+"/id/"+text).then(response => response.json())
    if(res["id"]==text){
      console.log('Login Successful');
      setBackgroundColor('green')
      setTimeout(()=>{navigation.navigate('Recorder',{cmd:true,id:text})},1000)
      // navigation.navigate('Recorder',{cmd:true,id:text});
    }
    else{
      setBackgroundColor("red");
      setTimeout(() => {setBackgroundColor("#f2f2f2")},500)
      
      console.log('Login Failed',res['id']);
    }
    
  }
  return (
    <View style={{ flex: 1,flexDirection: 'column',
    justifyContent: 'space-between',alignItems: 'stretch',paddingHorizontal:50, justifyContent: 'center' }}>
      <View style={{backgroundColor:background,marginBottom:5}}>
      <TextInput
        style={styles.input}
        onChangeText={(text)=>{console.log("Text Changed "+text);setText(text)}}
        value={text}
        placeholder='Enter Unique ID here'
        autoFocus
      />
      </View>
      <Button
        title="Login"
        onPress={onBth}
      />
    </View>
  );
}


const styles = StyleSheet.create({
  input: {
    height: 40,
    borderWidth: 1,
  },
});
