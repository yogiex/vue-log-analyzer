import { defineStore } from "pinia";
import { getAuth, onAuthStateChanged } from "firebase/auth";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    isLoading: true, // Untuk mendeteksi apakah status auth sedang diproses
  }),
  actions: {
    initializeAuth() {
      const auth = getAuth();
      this.isLoading = true;

      onAuthStateChanged(auth, (user) => {
        this.user = user;
        this.isLoading = false;
      });
    },
  },
});
