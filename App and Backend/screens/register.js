import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { Button } from '../components/button';
export default function Register({ navigation }) {
  

  return (
    
    <View style={{ flex: 1, alignItems: 'stretch',paddingHorizontal:50, justifyContent: 'center' }}>
      <Text style={styles.text}>From next screen you will be asked to speak 10 sentences which will be used by the model to learn about your voice</Text>
      <Button
        title="Next"
        onPress={() => navigation.navigate('Recorder',{cmd:false,id:-1})}
      />
    </View>
  );
}


const styles = StyleSheet.create({
  text: {
    fontSize: 16,
    lineHeight: 21,
    fontWeight: 'bold',
    letterSpacing: 0.25,
    color: 'black',
    textAlign:'justify',
    marginVertical:10,
  },
})