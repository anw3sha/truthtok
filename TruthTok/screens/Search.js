import React, { useState } from 'react';
import { StyleSheet, TextInput, TouchableOpacity, Text, View } from 'react-native';

const SearchScreen = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = () => {
    // Replace this with your search logic
    console.log('Searching for:', searchTerm);
    // You can navigate to a results screen or filter a list based on the search term here
  };

  return (
    <View style={styles.container}>
      <TextInput
        placeholder="Search an account..."
        value={searchTerm}
        onChangeText={text => setSearchTerm(text)}
        style={styles.input}
      />

      <TouchableOpacity onPress={handleSearch} style={styles.button}>
        <Text style={styles.buttonText}>Search</Text>
      </TouchableOpacity>
    </View>
  );
};

export default SearchScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  input: {
    width: '100%',
    backgroundColor: 'white',
    paddingHorizontal: 15,
    paddingVertical: 10,
    borderRadius: 10,
    marginBottom: 20,
    borderColor: '#ccc',
    borderWidth: 1,
  },
  button: {
    backgroundColor: '#0782F9',
    width: '100%',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontWeight: '700',
    fontSize: 16,
  },
});
