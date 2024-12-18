<script setup>
import { ref } from "vue";
import LoginForm from "@/layouts/LoginForm.vue";
import RegisterForm from "@/layouts/RegisterForm.vue";


const showRegister = ref(false);

const switchToRegister = () => (showRegister.value = true);
</script>



<template>
  <v-container
    fluid
    class="fill-height d-flex justify-center align-center"
  >
    <v-row justify="center" align="center" class="w-100">
      <v-col cols="12" sm="8" md="6" lg="4">
        <!-- Login Form Card -->
        <v-card class="custom-card px-10" elevation="8">
          <login-form>
            <template #footer>
              <v-card-text class="text-center mt-3 mb-5">
                <span class="text-center font-weight-light">
                  Don't have an account?
                </span>
                <span
                  class="text-blue-lighten-2 text-decoration-none cursor-pointer"
                  @click="switchToRegister"
                >
                  Register
                </span>
              </v-card-text>
            </template>
          </login-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

  <!-- Dialog for Register Form -->
  <v-dialog v-model="showRegister" persistent max-width="550px">
    <v-card-text>
      <register-form v-model="showRegister">
        <template #footer></template>
      </register-form>
    </v-card-text>
  </v-dialog>
</template>


<style scoped>
.custom-card {
  background-color: #000; /* Black background */
  color: #fff; /* White text color for contrast */
  border-radius: 20px; /* Rounded corners */
}
.fill-height {
  background-color: rgb(97, 43, 42); /* Background color for the entire page */
  margin: 0;
  padding: 0;
}
::v-deep(.v-overlay__scrim) {
  backdrop-filter: blur(40px) !important;
  background-color: rgba(0, 0, 0, 0.3) !important;
}
</style>




