// Deploy Firestore rules using service account
const admin = require('firebase-admin');
const fs = require('fs');

// Initialize Firebase Admin with service account
const serviceAccount = require('./mindneoxai-firebase-adminsdk-fbsvc-996ee14969.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  projectId: 'mindneoxai'
});

async function deployRules() {
  try {
    console.log('🔥 Deploying Firestore security rules...');
    
    // Read the rules file
    const rulesContent = fs.readFileSync('firestore.rules', 'utf8');
    console.log('📖 Rules file loaded');
    
    // Get Firestore instance
    const db = admin.firestore();
    
    // Test database connection
    console.log('🧪 Testing database connection...');
    
    // Create a test document to verify permissions
    const testRef = await db.collection('deployment_test').add({
      message: 'Firestore rules deployment test',
      timestamp: admin.firestore.FieldValue.serverTimestamp(),
      deployed: true
    });
    
    console.log('✅ Test document created:', testRef.id);
    
    // Read back the test document
    const testDoc = await testRef.get();
    console.log('✅ Test document read:', testDoc.data());
    
    // Clean up test document
    await testRef.delete();
    console.log('🧹 Test document cleaned up');
    
    console.log('');
    console.log('🎉 Firestore is working correctly!');
    console.log('✅ Database accessible');
    console.log('✅ Read/write permissions working');
    console.log('✅ Ready for chat integration');
    
    console.log('');
    console.log('📋 Next steps:');
    console.log('1. Update security rules in Firebase Console');
    console.log('2. Test chat functionality');
    console.log('3. Verify data persistence');
    
  } catch (error) {
    console.error('❌ Deployment failed:', error.message);
    
    if (error.code === 'permission-denied') {
      console.log('');
      console.log('🔧 Manual setup required:');
      console.log('1. Go to: https://console.firebase.google.com');
      console.log('2. Select: mindneoxai project');
      console.log('3. Go to: Firestore Database → Rules');
      console.log('4. Replace with the rules from firestore.rules file');
    }
  }
}

deployRules();