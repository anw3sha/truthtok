import { useNavigation } from '@react-navigation/native';
import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity } from 'react-native';
import Clipboard from '@react-native-clipboard/clipboard';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view';
import { auth } from '../firebase';
import { processLink } from '../authService';

const HomeScreen = () => {
  const [link, setLink] = useState('');
  const navigation = useNavigation();

  const handleAnalyze = () => {
    if (link.trim()) {
      console.log('Analyzing link:', link);
      processLink(link);
    } else {
      alert('Please enter a valid link');
    }
  };

  const handlePaste = async () => {
    const pastedLink = await Clipboard.getString();
    setLink(pastedLink);
  };

  const handleKeyDown = (event) => {
    const isPasteShortcut = (Platform.OS === 'macos' && event.metaKey && event.key === 'v') ||
                            (Platform.OS !== 'macos' && event.ctrlKey && event.key === 'v');
    if (isPasteShortcut) {
      handlePaste();
    }
  };

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Enter Link for Analysis:</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter TikTok video link"
        value={link}
        onChangeText={text => setLink(text)}
        multiline={true} 
        numberOfLines={1}
        keyboardType="url"
      />

      <TouchableOpacity onPress={handleAnalyze} style={styles.analyzeButton}>
        <Text style={styles.analyzeButtonText}>Analyze</Text>
      </TouchableOpacity>
      {/* <NavBar /> */}
    </View>
  );
};

export default HomeScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    marginTop: 20,
    marginBottom: 10,
  },
  input: {
    backgroundColor: 'white',
    paddingHorizontal: 15,
    paddingVertical: 10,
    borderRadius: 10,
    width: '100%',
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#ccc',
  },
  analyzeButton: {
    backgroundColor: '#0782F9',
    width: '60%',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 40,
  },
  analyzeButtonText: {
    color: 'white',
    fontWeight: '700',
    fontSize: 16,
  },
});