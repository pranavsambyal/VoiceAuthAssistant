// In App.js in a new project

import * as React from 'react';
import { View, Text,Button } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import {backend} from './screens/consts';


function DetailsScreen({ navigation }) {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Details Screen</Text>
      <Button
        title="Go to Details... again"
        onPress={() => navigation.navigate('Home')}
      />
    </View>
  );
}

import Start from './screens/start'
import Login from './screens/login'
import Register from './screens/register'
import Recorder from './screens/recorder';
function HomeScreen({navigation}) {
  return (
    <View style={{ flex: 1, alignItems: 'stretch',paddingHorizontal:50, justifyContent: 'center' ,backgroundColor:"#ffffff"}}>
          <Text>Home Screen</Text>
          <Button
            title="Go to Details"
            onPress={() => navigation.navigate('Details')}
          />
        </View>
  );
}

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator  initialRouteName="Home">
        <Stack.Screen name="Home" component={Start} />
        <Stack.Screen name="Details" component={DetailsScreen} />
        <Stack.Screen name="Register" component={Register} />
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Recorder" component={Recorder} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;