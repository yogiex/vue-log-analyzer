// Utilities
import { defineStore } from 'pinia'
import { auth } from '../firebase'
import { signInWithEmailAndPassword, signOut, onAuthStateChanged} from 'firebase/auth'
export const useAppStore = defineStore('app', {
  id: 'storeApp',
  state: () => {
    return {
      email: '',
      password: '',
    }
  },
  getters: {},
  actions: {
    async login(){
      try {
        const res = await signInWithEmailAndPassword(auth,this.email,this.password)
        if(res) {
          
        }
      } catch (error) {
        console.log(error)
      }
    }
  }
})
