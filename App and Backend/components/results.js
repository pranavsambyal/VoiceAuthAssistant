import React from 'react';
import { View, ScrollView, Text, StyleSheet } from 'react-native';

const ScrollableTextBox = ({ data }) => {
  if (!data) {
    // If there is no data, render null or any other placeholder
    return null;
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text>{data}</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex:0.3,
    padding: 10,
  },
});

export default ScrollableTextBox;
