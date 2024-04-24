/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from "@/plugins";

// Components
import App from "./App.vue";

// Composables
import { createApp } from "vue";

// Import the functions you need from the SDKs you need

import { initializeApp } from "firebase/app";

// TODO: Add SDKs for Firebase products that you want to use

// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration

const firebaseConfig = {
  apiKey: "AIzaSyBRrGPqQrvC4o2Ij3mF_jvmOO30l9xvlIU",

  authDomain: "vue-auth-analyzer.firebaseapp.com",

  projectId: "vue-auth-analyzer",

  storageBucket: "vue-auth-analyzer.appspot.com",

  messagingSenderId: "980989288707",

  appId: "1:980989288707:web:373b7a8dd2bc2beb3d4936",
};
// Initialize Firebase

initializeApp(firebaseConfig);

const app = createApp(App);

registerPlugins(app);

app.mount("#app");
