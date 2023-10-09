import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View ,Pressable} from 'react-native';

const Separator = () => <View style={styles.separator} />;
import { Button } from '../components/button';
export default function Start({navigation}) {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Click Register button to register your voice sample</Text>
      <Button onPress={()=>{navigation.navigate('Register')}} title="Register"></Button>
<Separator />
<Text style={styles.text}>Click login button to login with your unique ID</Text>
<Button onPress={()=>{navigation.navigate('Login')}} title="Login"></Button>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'stretch',
    paddingHorizontal:50,
    justifyContent: 'center',
  },
  fixToText: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },separator: {
    marginVertical: 10,
    borderBottomColor: '#737373',
    borderBottomWidth: StyleSheet.hairlineWidth,
  },button: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 32,
    borderRadius: 4,
    elevation: 3,
    backgroundColor: 'black',
    marginTop:10,
  },
  text: {
    fontSize: 16,
    lineHeight: 21,
    fontWeight: 'bold',
    letterSpacing: 0.25,
    color: 'black',
    textAlign:'center',
    marginVertical:10,
  },
});
  