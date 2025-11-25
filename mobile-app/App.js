import React, { useState, useEffect, useRef } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  Alert,
  Animated,
  Dimensions,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { LinearGradient } from 'expo-linear-gradient';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Speech from 'expo-speech';
import axios from 'axios';

const API_BASE = 'https://yeduru-abhi.hf.space'; // Your Hugging Face backend
const { width, height } = Dimensions.get('window');

// Splash Screen Component
function SplashScreen({ onFinish }) {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    // Animate splash screen
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        tension: 50,
        friction: 7,
        useNativeDriver: true,
      }),
    ]).start();

    // Auto-dismiss after 2.5 seconds
    const timer = setTimeout(() => {
      Animated.timing(fadeAnim, {
        toValue: 0,
        duration: 500,
        useNativeDriver: true,
      }).start(() => onFinish());
    }, 2500);

    return () => clearTimeout(timer);
  }, []);

  return (
    <View style={styles.splashContainer}>
      <LinearGradient
        colors={['#0f0f0f', '#1a1a2e', '#16213e']}
        style={styles.splashGradient}
      >
        <Animated.View
          style={[
            styles.splashContent,
            {
              opacity: fadeAnim,
              transform: [{ scale: scaleAnim }],
            },
          ]}
        >
          {/* Logo/Icon */}
          <View style={styles.logoContainer}>
            <LinearGradient
              colors={['#3b82f6', '#8b5cf6', '#ec4899']}
              style={styles.logoGradient}
            >
              <Text style={styles.logoText}>MN</Text>
            </LinearGradient>
          </View>

          {/* App Name */}
          <Text style={styles.splashTitle}>MindNeox AI</Text>
          <Text style={styles.splashSubtitle}>Your Intelligent Assistant</Text>

          {/* Loading Indicator */}
          <ActivityIndicator
            color="#60a5fa"
            size="small"
            style={styles.splashLoader}
          />
        </Animated.View>
      </LinearGradient>
    </View>
  );
}

// Main Chat App Component
function ChatApp() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! I'm MindNeox AI. How can I help you today?",
      timestamp: new Date().toISOString(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const scrollViewRef = useRef(null);

  useEffect(() => {
    loadMessages();
  }, []);

  useEffect(() => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  }, [messages]);

  const loadMessages = async () => {
    try {
      const saved = await AsyncStorage.getItem('messages');
      if (saved) {
        setMessages(JSON.parse(saved));
      }
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const saveMessages = async (newMessages) => {
    try {
      await AsyncStorage.setItem('messages', JSON.stringify(newMessages));
    } catch (error) {
      console.error('Error saving messages:', error);
    }
  };

  const handleSend = async () => {
    const textToSend = input.trim();
    if (!textToSend || isLoading) return;

    const userMessage = {
      role: 'user',
      content: textToSend,
      timestamp: new Date().toISOString(),
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/api/chat`, {
        message: textToSend,
        user_id: 'mobile_user',
        conversation_id: 'default',
      });

      const botContent = response.data.response || 'I received your message!';
      const botMessage = {
        role: 'assistant',
        content: botContent,
        timestamp: new Date().toISOString(),
      };

      const finalMessages = [...updatedMessages, botMessage];
      setMessages(finalMessages);
      saveMessages(finalMessages);
    } catch (error) {
      console.error('Send error:', error);
      Alert.alert('Error', 'Failed to send message. Please try again.');
      setMessages(updatedMessages);
    } finally {
      setIsLoading(false);
    }
  };

  const speakMessage = (text) => {
    Speech.speak(text, {
      language: 'en',
      pitch: 1.0,
      rate: 0.9,
    });
  };

  const clearChat = () => {
    Alert.alert('Clear Chat', 'Are you sure you want to clear all messages?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Clear',
        style: 'destructive',
        onPress: () => {
          const welcomeMessage = {
            role: 'assistant',
            content: "Hello! I'm MindNeox AI. How can I help you today?",
            timestamp: new Date().toISOString(),
          };
          setMessages([welcomeMessage]);
          saveMessages([welcomeMessage]);
        },
      },
    ]);
  };

  return (
    <View style={styles.container}>
      <StatusBar style="light" />

      {/* Header */}
      <LinearGradient colors={['#1a1a2e', '#16213e']} style={styles.header}>
        <Text style={styles.headerTitle}>MindNeox AI</Text>
        <TouchableOpacity onPress={clearChat} style={styles.clearButton}>
          <Text style={styles.clearButtonText}>Clear</Text>
        </TouchableOpacity>
      </LinearGradient>

      {/* Messages */}
      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
      >
        {messages.map((message, index) => (
          <View
            key={index}
            style={[
              styles.messageBubble,
              message.role === 'user' ? styles.userBubble : styles.aiBubble,
            ]}
          >
            {message.role === 'assistant' && (
              <Text style={styles.aiLabel}>MindNeox</Text>
            )}
            <Text
              style={[
                styles.messageText,
                message.role === 'user' ? styles.userText : styles.aiText,
              ]}
            >
              {message.content}
            </Text>
            {message.role === 'assistant' && (
              <TouchableOpacity
                onPress={() => speakMessage(message.content)}
                style={styles.speakButton}
              >
                <Text style={styles.speakButtonText}>🔊 Speak</Text>
              </TouchableOpacity>
            )}
            <Text style={styles.timestamp}>
              {new Date(message.timestamp).toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit',
              })}
            </Text>
          </View>
        ))}

        {isLoading && (
          <View style={styles.loadingBubble}>
            <Text style={styles.aiLabel}>MindNeox</Text>
            <ActivityIndicator color="#60a5fa" size="small" />
            <Text style={styles.loadingText}>Thinking...</Text>
          </View>
        )}
      </ScrollView>

      {/* Input Area */}
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.inputContainer}
      >
        <View style={styles.inputWrapper}>
          <TextInput
            style={styles.input}
            value={input}
            onChangeText={setInput}
            placeholder="Message MindNeox..."
            placeholderTextColor="#6b7280"
            multiline
            maxLength={500}
            editable={!isLoading}
          />
          <TouchableOpacity
            onPress={handleSend}
            disabled={!input.trim() || isLoading}
            style={[
              styles.sendButton,
              (!input.trim() || isLoading) && styles.sendButtonDisabled,
            ]}
          >
            <Text style={styles.sendButtonText}>Send</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </View>
  );
}

// Main App Component with Splash Screen
export default function App() {
  const [showSplash, setShowSplash] = useState(true);

  if (showSplash) {
    return <SplashScreen onFinish={() => setShowSplash(false)} />;
  }

  return <ChatApp />;
}

const styles = StyleSheet.create({
  // Splash Screen Styles
  splashContainer: {
    flex: 1,
  },
  splashGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  splashContent: {
    alignItems: 'center',
  },
  logoContainer: {
    marginBottom: 30,
  },
  logoGradient: {
    width: 100,
    height: 100,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#3b82f6',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.5,
    shadowRadius: 20,
    elevation: 10,
  },
  logoText: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#fff',
  },
  splashTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  splashSubtitle: {
    fontSize: 16,
    color: '#9ca3af',
    marginBottom: 40,
  },
  splashLoader: {
    marginTop: 20,
  },

  // Chat App Styles
  container: {
    flex: 1,
    backgroundColor: '#0f0f0f',
  },
  header: {
    paddingTop: Platform.OS === 'ios' ? 50 : 40,
    paddingBottom: 15,
    paddingHorizontal: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.1)',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  clearButton: {
    paddingHorizontal: 15,
    paddingVertical: 8,
    backgroundColor: 'rgba(239, 68, 68, 0.2)',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(239, 68, 68, 0.3)',
  },
  clearButtonText: {
    color: '#fca5a5',
    fontSize: 14,
    fontWeight: '600',
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 16,
  },
  messageBubble: {
    marginBottom: 16,
    padding: 16,
    borderRadius: 20,
    maxWidth: '85%',
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: 'rgba(59, 130, 246, 0.2)',
    borderWidth: 1,
    borderColor: 'rgba(59, 130, 246, 0.3)',
  },
  aiBubble: {
    alignSelf: 'flex-start',
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  aiLabel: {
    fontSize: 11,
    fontWeight: '600',
    color: '#60a5fa',
    marginBottom: 6,
  },
  messageText: {
    fontSize: 15,
    lineHeight: 22,
  },
  userText: {
    color: '#e0e7ff',
  },
  aiText: {
    color: '#f3f4f6',
  },
  timestamp: {
    fontSize: 10,
    color: 'rgba(255, 255, 255, 0.4)',
    marginTop: 8,
    textAlign: 'right',
  },
  speakButton: {
    marginTop: 8,
    paddingVertical: 6,
    paddingHorizontal: 12,
    backgroundColor: 'rgba(96, 165, 250, 0.2)',
    borderRadius: 8,
    alignSelf: 'flex-start',
  },
  speakButtonText: {
    color: '#60a5fa',
    fontSize: 12,
    fontWeight: '600',
  },
  loadingBubble: {
    alignSelf: 'flex-start',
    padding: 16,
    borderRadius: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
    maxWidth: '85%',
  },
  loadingText: {
    color: '#9ca3af',
    fontSize: 14,
    marginTop: 8,
  },
  inputContainer: {
    borderTopWidth: 1,
    borderTopColor: 'rgba(255, 255, 255, 0.1)',
    backgroundColor: '#1a1a1a',
  },
  inputWrapper: {
    flexDirection: 'row',
    padding: 12,
    alignItems: 'flex-end',
  },
  input: {
    flex: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.08)',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 12,
    color: '#fff',
    fontSize: 15,
    maxHeight: 100,
    marginRight: 8,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.15)',
  },
  sendButton: {
    backgroundColor: '#3b82f6',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: 'rgba(59, 130, 246, 0.3)',
  },
  sendButtonText: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '600',
  },
});
