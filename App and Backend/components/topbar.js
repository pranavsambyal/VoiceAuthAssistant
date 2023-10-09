import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const TopBarComponent = ({ title }) => {
  return (
    <View style={styles.container}>
      <View style={styles.topBar}>
        <Text style={styles.title}>{title}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent:'space-between',
  },
  topBar: {
    marginTop:40,
    backgroundColor: '#f2f2f2',
    paddingVertical: 10,
    paddingHorizontal: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign:'center',
  },
});

export default TopBarComponent;
