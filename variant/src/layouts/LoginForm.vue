<script>
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const authStore = useAuthStore(); // Access the auth store
    const router = useRouter(); // Router instance for navigation
    const email = ref("");
    const password = ref("");
    const visible = ref(false);

    const handleLogin = async () => {
      const success = await authStore.login(email.value, password.value);
      if (success) {
        if (email.value === "admin@gmail.com") {
          // Admin goes to dashboard
          localStorage.setItem("activeTab", "dashboard");
          router.push("/dashboard"); // Navigate to the dashboard
        } else {
          // Non-admin goes to chats
          localStorage.setItem("activeTab", "chats");
          router.push("/app2"); // Navigate to the dashboard
        }
      } else {
        alert("Login failed. Please check your credentials.");
      }
    };

    return { email, password, handleLogin, visible };
  },
};
</script>




<template>
    <v-img
      src="/sendease.png"
      alt="SendEase Logo"
      contain
      class="logo my-9"
      style="width: 100%; height: 100px; margin: 0 auto;"
    ></v-img>
  <v-card class="bg-card custom-card" elevation="8">


    <v-form class="mt-3" ref="form" @submit.prevent="handleLogin">
  <!-- Email Field -->
  <v-text-field
    v-model="email" 
    density="compact"
    label="Email"
    type="email"
    prepend-inner-icon="mdi-email-outline"
    variant="outlined"
    required
  ></v-text-field>

  <!-- Password Field -->
  <v-text-field
    v-model="password" 
    :append-inner-icon="visible ? 'mdi-eye' : 'mdi-eye-off'"
    :type="visible ? 'text' : 'password'"
    density="compact"
    label="Password"
    prepend-inner-icon="mdi-lock-outline"
    variant="outlined"
    @click:append-inner="visible = !visible"
    required
  ></v-text-field>

  <v-btn type="submit" class="mt-1" size="large" block>
    Login
  </v-btn>
</v-form>

    <slot name="footer" />
  </v-card>
</template>

<style scoped>
@import url('https://fonts.cdnfonts.com/css/unbounded');
@import url('https://fonts.cdnfonts.com/css/wix-madefor-display');
.custom-card {
  background-color: black; /* Set card/form background to black */
  color: white; /* Text color to white for contrast */
  border-radius: 12px; /* Optional: rounded corners for aesthetics */
}
.v-btn{
  background-color: rgb(97, 43, 42);
}
.title{
  font-family: 'Unbounded', Arial, sans-serif;
}
.v-form{
  font-family: 'Wix Madefor Display', sans-serif;                              
}

</style>