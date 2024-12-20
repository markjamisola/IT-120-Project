<template>
  <v-card class=" custom-card px-8" elevation="8">
    <v-img
      src="/sendease.png"
      alt="SendEase Logo"
      contain
      class="logo mt-3"
      style="width: 70%; height: 100px; margin: 0 auto;"
    ></v-img>
    <h2 class="text-center pt-6 pb-4">Create an account</h2>
    <v-form ref="form" @submit.prevent="handleRegister">
      <v-text-field
        v-model="username"
        label="Username"
        required
        variant="outlined"
        prepend-inner-icon="mdi-account-outline"
      />
      <v-text-field
        v-model="email"
        label="Email"
        type="email"
        required
        variant="outlined"
        prepend-inner-icon="mdi-email-outline"
      />
      <v-text-field
        v-model="password"
        label="Password"
        :type="passwordVisible ? 'text' : 'password'"
        required
        variant="outlined"
        prepend-inner-icon="mdi-lock-outline"
        :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append-inner="passwordVisible = !passwordVisible"
      />

      <v-text-field
        v-model="confirmPassword"
        label="Confirm Password"
        :type="confirmPasswordVisible ? 'text' : 'password'"
        required
        variant="outlined"
        prepend-inner-icon="mdi-lock-outline"
        :append-inner-icon="confirmPasswordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append-inner="confirmPasswordVisible = !confirmPasswordVisible"
      />

      <v-row class="pb-10 pt-2">
        <v-col>
          <v-btn @click="handleBack" color="white" block>Back</v-btn>
        </v-col>
        <v-col>
          <v-btn type="submit" block>Submit</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-card>
</template>

<script>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

export default {
  props: {
    modelValue: Boolean,
  },
  emits: ["update:modelValue"],

  setup(props, { emit }) {
    const authStore = useAuthStore();
    const username = ref("");
    const email = ref("");
    const toast = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const passwordVisible = ref(false); // For toggling password visibility
    const confirmPasswordVisible = ref(false); // For toggling confirm password visibility

    const handleRegister = async () => {
      if (
        !username.value ||
        !email.value ||
        !password.value ||
        !confirmPassword.value
      ) {
        toast("Please fill out all fields.");
        return false;
      }

      const success = await authStore.register(
        username.value,
        email.value,
        password.value,
        confirmPassword.value
      );

      if (success) {
        emit("update:modelValue", false); // Close dialog after successful registration
      }
    };

    const handleBack = () => {
      emit("update:modelValue", false); // Close the dialog without registering
    };

    return {
      username,
      email,
      password,
      confirmPassword,
      passwordVisible,
      confirmPasswordVisible,
      handleRegister,
      handleBack,
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.cdnfonts.com/css/unbounded');
@import url('https://fonts.cdnfonts.com/css/wix-madefor-display');
.custom-card {
  background-color: black; /* Set card/form background to black */
  color: white; /* Text color to white for contrast */
  border-radius: 20px; /* Optional: rounded corners for aesthetics */
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
