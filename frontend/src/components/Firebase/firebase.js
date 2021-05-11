import firebase from 'firebase/app';
import 'firebase/storage';

// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyAZ0Ehttva5SujoIHlZh4X4tEv96nMUzyo",
    authDomain: "brain-tumor-detection-aa187.firebaseapp.com",
    projectId: "brain-tumor-detection-aa187",
    storageBucket: "brain-tumor-detection-aa187.appspot.com",
    messagingSenderId: "104567495340",
    appId: "1:104567495340:web:4fbdb8d8c51055f63a1d09",
    measurementId: "G-7MJYX9XXNZ"
  };

  firebase.initializeApp(firebaseConfig);

  const storage = firebase.storage();

  export { storage, firebase as default };


// <!-- The core Firebase JS SDK is always required and must be listed first -->
// <script src="/__/firebase/8.5.0/firebase-app.js"></script>

// <!-- TODO: Add SDKs for Firebase products that you want to use
//      https://firebase.google.com/docs/web/setup#available-libraries -->
// <script src="/__/firebase/8.5.0/firebase-analytics.js"></script>

// <!-- Initialize Firebase -->
// <script src="/__/firebase/init.js"></script>