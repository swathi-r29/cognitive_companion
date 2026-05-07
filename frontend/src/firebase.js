import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyA3TLYqN77I2_V83dy3hIWLaML9iUdhl6g",
  authDomain: "cognitive-mood.firebaseapp.com",
  projectId: "cognitive-mood",
  storageBucket: "cognitive-mood.firebasestorage.app",
  messagingSenderId: "866761662761",
  appId: "1:866761662761:web:77e43ef4d269ff49525738",
  measurementId: "G-J8S5CQXLY5"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const analytics = typeof window !== 'undefined' ? getAnalytics(app) : null;
export default app;
