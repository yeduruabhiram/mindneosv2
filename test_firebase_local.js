// Simple Firebase test for Node.js
const { initializeApp } = require('firebase/app');
const { getFirestore, collection, addDoc, getDocs } = require('firebase/firestore');

const firebaseConfig = {
  apiKey: "AIzaSyBQtb9AVk4zaGdbFr-KArUvtJAIzwmJF_g",
  authDomain: "mindneoxai.firebaseapp.com",
  projectId: "mindneoxai",
  storageBucket: "mindneoxai.firebasestorage.app",
  messagingSenderId: "432980643521",
  appId: "1:432980643521:web:29aa3a269a4301e19f8e40"
};

async function testFirebase() {
  try {
    console.log('🔥 Initializing Firebase...');
    const app = initializeApp(firebaseConfig);
    const db = getFirestore(app);
    
    console.log('✅ Firebase initialized successfully');
    console.log('📊 Project ID:', firebaseConfig.projectId);
    
    // Test basic connection
    console.log('🧪 Testing Firestore connection...');
    
    // Try to add a test document
    const testData = {
      message: 'Firebase connection test',
      timestamp: new Date().toISOString(),
      source: 'local_test'
    };
    
    const docRef = await addDoc(collection(db, 'connection_test'), testData);
    console.log('✅ Test document created with ID:', docRef.id);
    
    // Try to read documents
    const querySnapshot = await getDocs(collection(db, 'connection_test'));
    console.log('✅ Found', querySnapshot.size, 'test documents');
    
    console.log('🎉 Firebase/Firestore connection successful!');
    console.log('');
    console.log('Ready for chat integration:');
    console.log('- ✅ Firebase config valid');
    console.log('- ✅ Firestore database accessible');
    console.log('- ✅ Read/write permissions working');
    
  } catch (error) {
    console.error('❌ Firebase test failed:');
    console.error('Error code:', error.code);
    console.error('Error message:', error.message);
    
    if (error.code === 'permission-denied') {
      console.log('');
      console.log('💡 Solution: Set up Firestore security rules');
      console.log('Go to Firebase Console → Firestore → Rules');
      console.log('Use these rules for testing:');
      console.log('');
      console.log('rules_version = \'2\';');
      console.log('service cloud.firestore {');
      console.log('  match /databases/{database}/documents {');
      console.log('    match /{document=**} {');
      console.log('      allow read, write: if true;');
      console.log('    }');
      console.log('  }');
      console.log('}');
    }
  }
}

// Run the test
testFirebase();