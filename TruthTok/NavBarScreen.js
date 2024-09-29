import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Icon } from 'react-native-elements'; 
import HomeScreen from './screens/HomeScreen';
import SearchScreen from './screens/Search';
import SettingsScreen from './screens/Settings';

const Tab = createBottomTabNavigator();

const AppNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#0782F9',
        tabBarInactiveTintColor: 'gray',
        headerShown: false,
      }}
    >
      <Tab.Screen 
        name="Home" 
        component={HomeScreen} 
        options={{
          tabBarIcon: ({ color }) => (
            <Icon name="home" type="font-awesome" color={color} />
          ),
        }} 
      />
      <Tab.Screen 
        name="Search" 
        component={SearchScreen} 
        options={{
          tabBarIcon: ({ color }) => (
            <Icon name="search" type="font-awesome" color={color} />
          ),
        }} 
      />
      <Tab.Screen 
        name="Settings" 
        component={SettingsScreen} 
        options={{
          tabBarIcon: ({ color }) => (
            <Icon name="cogs" type="font-awesome" color={color} />
          ),
        }} 
      />
    </Tab.Navigator>
  );
};

export default AppNavigator;
