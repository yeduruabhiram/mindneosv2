// Test Firestore connection
import { initializeApp } from 'firebase/app'
import { getFirestore, collection, addDoc, getDocs } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: "AIzaSyBQtb9AVk4zaGdbFr-KArUvtJAIzwmJF_g",
  authDomain: "mindneoxai.firebaseapp.com",
  projectId: "mindneoxai",
  storageBucket: "mindneoxai.firebasestorage.app",
  messagingSenderId: "432980643521",
  appId: "1:432980643521:web:29aa3a269a4301e19f8e40"
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)
const db = getFirestore(app)

async function testFirestore() {
  try {
    console.log('Testing Firestore connection...')
    
    // Test write
    const docRef = await addDoc(collection(db, 'test'), {
      message: 'Hello Firestore!',
      timestamp: new Date(),
      test: true
    })
    console.log('✅ Document written with ID:', docRef.id)
    
    // Test read
    const querySnapshot = await getDocs(collection(db, 'test'))
    console.log('✅ Documents found:', querySnapshot.size)
    
    querySnapshot.forEach((doc) => {
      console.log('Document:', doc.id, '=>', doc.data())
    })
    
    console.log('🎉 Firestore connection successful!')
    
  } catch (error) {
    console.error('❌ Firestore connection failed:', error)
  }
}

// Run test
testFirestore()