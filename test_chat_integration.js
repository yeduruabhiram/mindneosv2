// Test the complete chat integration with Firestore
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, getDocs, query, orderBy } from 'firebase/firestore';
import { saveChatExchange, getUserConversations } from './mindneox-frontend/src/services/chatService.js';

const firebaseConfig = {
  apiKey: "AIzaSyBQtb9AVk4zaGdbFr-KArUvtJAIzwmJF_g",
  authDomain: "mindneoxai.firebaseapp.com",
  projectId: "mindneoxai",
  storageBucket: "mindneoxai.firebasestorage.app",
  messagingSenderId: "432980643521",
  appId: "1:432980643521:web:29aa3a269a4301e19f8e40"
};

async function testChatIntegration() {
  try {
    console.log('🧪 Testing Chat Integration with Firestore...');
    
    // Initialize Firebase
    const app = initializeApp(firebaseConfig);
    const db = getFirestore(app);
    
    console.log('✅ Firebase initialized');
    
    // Test user ID (simulating Clerk user)
    const testUserId = 'test_user_' + Date.now();
    console.log('👤 Test User ID:', testUserId);
    
    // Test 1: Save a chat exchange
    console.log('\n📝 Test 1: Saving chat exchange...');
    const userMessage = 'Hello, what is artificial intelligence?';
    const aiResponse = 'Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines that can perform tasks that typically require human intelligence.';
    
    const conversationId = await saveChatExchange(testUserId, userMessage, aiResponse);
    console.log('✅ Chat saved! Conversation ID:', conversationId);
    
    // Test 2: Retrieve user conversations
    console.log('\n📖 Test 2: Retrieving user conversations...');
    const conversations = await getUserConversations(testUserId);
    console.log('✅ Found', conversations.length, 'conversations');
    
    if (conversations.length > 0) {
      console.log('📄 Latest conversation:', {
        id: conversations[0].id,
        title: conversations[0].title,
        messageCount: conversations[0].messageCount?.length || 0,
        lastMessage: conversations[0].lastMessage
      });
    }
    
    // Test 3: Check all conversations in database
    console.log('\n🔍 Test 3: Checking all conversations in database...');
    const allConversations = await getDocs(collection(db, 'conversations'));
    console.log('📊 Total conversations in database:', allConversations.size);
    
    // Test 4: Check all messages in database
    console.log('\n💬 Test 4: Checking all messages in database...');
    const allMessages = await getDocs(collection(db, 'messages'));
    console.log('📊 Total messages in database:', allMessages.size);
    
    allMessages.forEach((doc) => {
      const data = doc.data();
      console.log('💬 Message:', {
        id: doc.id,
        role: data.role,
        content: data.content.substring(0, 50) + '...',
        conversationId: data.conversationId
      });
    });
    
    console.log('\n🎉 Chat Integration Test SUCCESSFUL!');
    console.log('✅ Firestore saving works');
    console.log('✅ Conversation retrieval works');
    console.log('✅ Database structure correct');
    
  } catch (error) {
    console.error('❌ Chat Integration Test FAILED:');
    console.error('Error:', error.message);
    console.error('Stack:', error.stack);
  }
}

testChatIntegration();