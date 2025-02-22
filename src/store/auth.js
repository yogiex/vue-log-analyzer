import { defineStore } from "pinia";
import {
  getAuth,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut,
} from "firebase/auth";
import { ref } from "vue";
import { useRouter } from "vue-router";
export const useAuthStore = defineStore("authStore", () => {
  const auth = getAuth();
  const user = ref({});
  const router = useRouter();

  const init = () => {
    onAuthStateChanged(auth, (userDetails) => {
      console.log("auth state changed");
      console.log(userDetails);

      if (userDetails) {
        const uid = userDetails.uid;
        user.value = { email: userDetails.email, uid, userDetails };
        console.log(user);
      } else {
        user.value = {}; // Reset the user to an empty object when not authenticated
      }

      if (!userDetails) {
        router.push("/login");
      }
    });
  };

  const loginUser = (credentials) => {
    signInWithEmailAndPassword(auth, credentials.email, credentials.password)
      .then((userCredentials) => {
        const user = userCredentials.user;
        router.push("/dashboard");
        console.log(user);
      })
      .catch((error) => {
        console.log(error.message);
      });
  };

  const logOut = () => {
    signOut(auth)
      .then(() => {
        console.log("logged out");
        router.push("/login");
      })
      .catch((error) => {
        console.log(error.message);
      });
  };

  return { loginUser, logOut, init, user };
});
