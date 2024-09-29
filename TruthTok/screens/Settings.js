import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Alert } from 'react-native';
import { handleDeleteAccount } from '../firebase';

const CreatorProfileScreen = ({ route }) => {
  // Assuming data is passed as route params
  const { username, videosChecked, results } = route.params;
  const { trueCount, falseCount, maybeCount } = results;

  const deleteAccount = () => {
    Alert.alert(
      'Delete Account',
      'Are you sure you want to delete your account?',
      [ {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'OK',
          onPress: () => {
            try {
              handleDeleteAccount(); 
              console.log('Account deleted successfully');
              navigation.replace('Login');
            } catch (error) {
              alert(error.message);
            }
          },
        },
      ]
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.username}>{username}</Text>
      <Text style={styles.sectionTitle}>Videos Checked:</Text>
      <View style={styles.videoStatsContainer}>
        <Text style={styles.videoStat}>Total Videos: {videosChecked}</Text>
        <Text style={styles.videoStat}>True: {trueCount}</Text>
        <Text style={styles.videoStat}>False: {falseCount}</Text>
        <Text style={styles.videoStat}>Indeterminate: {maybeCount}</Text>
      </View>

      <TouchableOpacity
        onPress={deleteAccount}
        style={styles.deleteButton}
      >
        <Text style={styles.deleteButtonText}>Delete Account</Text>
      </TouchableOpacity>
    </View>
  );
};

export default CreatorProfileScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  username: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 10,
  },
  videoStatsContainer: {
    backgroundColor: '#f0f0f0',
    padding: 15,
    borderRadius: 10,
    width: '100%',
    alignItems: 'flex-start',
    marginBottom: 20,
  },
  videoStat: {
    fontSize: 16,
    marginVertical: 5,
  },
  deleteButton: {
    backgroundColor: '#ff4d4d',
    width: '80%',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  deleteButtonText: {
    color: 'white',
    fontWeight: '700',
    fontSize: 16,
  },
});
