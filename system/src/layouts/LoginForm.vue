<template>
  <v-card class="bg-card" elevation="8">
    <h1 class="text-center py-8">$Title Here</h1>

    <v-form ref="form" @submit.prevent="handleLogin">
      <v-text-field
        v-model="email"
        color="blue-lighten-2"
        label="Email"
        type="email"
        required
        outlined
      />
      <v-text-field
        v-model="password"
        color="blue-lighten-2"
        label="Password"
        type="password"
        required
        outlined
      />
      <v-btn type="submit" color="primary" class="mt-1" size="large" block
        >Login</v-btn
      >
    </v-form>
    <slot name="footer" />
  </v-card>
</template>

<script>
import { useAuthStore } from "@/stores/auth"; // Importing the merged auth store
import { ref } from "vue";
import { useRouter } from "vue-router";


export default {
  setup() {
    const authStore = useAuthStore(); // Access the auth store
    const router = useRouter();
    const email = ref(""); // Bind email input
    const password = ref(""); // Bind password input
   

    const handleLogin = async () => {
      const success = await authStore.login(email.value, password.value); // Use the store's login action
      if (!success) {
       alert("Login failed"); 
      } else {
       alert("Login successful"); 
        // Redirect to the previously requested page, or to /dashboard if none is specified
        const redirect =
          router.currentRoute.value.query.redirect || "/dashboard";
        router.push(redirect);
      }
    };

    return { email, password, handleLogin };
  },
};
</script>

<style scoped>

</style>
