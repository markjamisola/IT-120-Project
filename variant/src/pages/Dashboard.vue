<template>
  <v-app class="app-container">
    <!-- Top Navigation Bar -->
    <v-app-bar app color="#151515" class="px-5">
      <!-- App Title -->
      <v-toolbar-title class="text-h5 font-weight-black">Receiver</v-toolbar-title>
      
      <!-- Navigation Tabs -->
      <v-tabs v-model="activeTab" class="mx-5">
        <v-tab value="dashboard">
          <v-icon left class="me-1">mdi-view-dashboard</v-icon> Dashboard
        </v-tab>
        <v-tab value="chats">
          <v-icon left class="me-1">mdi-chat</v-icon> Receive a Message
        </v-tab>
      </v-tabs>
      
      <v-spacer></v-spacer>
      
      <!-- Notification Icon with Badge -->
      <v-btn size="x-small" variant="tonal" icon class="mr-3">
        <v-badge color="red" dot>
          <v-icon>mdi-bell</v-icon>
        </v-badge>
      </v-btn>
      
      <!-- User Settings Menu -->
      <v-menu transition="slide-y-transition">
        <template v-slot:activator="{ props }">
          <v-btn rounded="xl" size="large" variant="tonal" v-bind="props">
            <v-avatar size="25" class="mr-2"></v-avatar>
            <v-icon color="white">mdi-cog</v-icon>
          </v-btn>
        </template>
        
        <v-sheet class="pa-0 mt-2 me-1 menu-card" color="grey-darken-3">
          <div>
            
          
            <v-btn
              class="justify-start"
              rounded="0"
              variant="text"
              size="large"
              block
              @click="handleLogoutClick"
              style="text-transform: none"
            >
              <v-row align="center" no-gutters>
                <v-col cols="auto">
                  <v-icon class="me-3" left>mdi-logout</v-icon>
                </v-col>
                <v-col @click="logout"> Logout </v-col>
              </v-row>
            </v-btn>
          </div>
        </v-sheet>
      </v-menu>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="custom-main">
      <v-container fluid class="main-container pa-8 rounded-lg">
        <v-row v-if="activeTab === 'dashboard'">
          <v-col cols="12">
            <UserTable :userData="users" />
          </v-col>
        </v-row>
        <v-row v-else-if="activeTab === 'chats'">
          <v-col cols="12">
            <ChatBox />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth"; // Import the auth store
import UserTable from "@/views/dashboard/UserTable.vue";
import ChatBox from "@/components/ChatBox.vue"; // Import ChatBox component

const users = ref([]);
const activeTab = ref(localStorage.getItem("activeTab") || "dashboard"); // Retrieve activeTab from local storage

const fetchUsers = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/users/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });
    users.value = response.data.data.users.map((user) => ({
      username: user.name,
      email: user.email,
      status: "active",
    }));
  } catch (err) {
    console.error("Error fetching users:", err.message);
  }
};

const logout = () => {
  const authStore = useAuthStore();
  authStore.logout(); // Clear the auth token in Pinia store
};

onMounted(fetchUsers);

// Watch for changes in activeTab and save it to local storage
watch(activeTab, (newTab) => {
  localStorage.setItem("activeTab", newTab);
});
</script>

<style scoped>
.custom-main {
  padding-top: 64px; /* To account for the app bar height */
}
</style>
