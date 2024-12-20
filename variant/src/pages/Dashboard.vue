<template>
  <v-app class="app-container">
    <!-- Top Navigation Bar -->
    <div class="fixed-header">
      <v-app-bar app color="black navbar" class="px-5 py-1">
        <v-toolbar-title class="text-h5 font-weight-black title text-white">SendEase</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn rounded="xl" size="large" variant="tonal" @click="showLogoutConfirmation">
          <v-icon color="white" left>mdi-logout</v-icon> Logout
        </v-btn>
        <v-dialog v-model="logoutModal" max-width="400">
          <v-card class="mx-auto pa-3" elevation="15" rounded="lg" color="black">
            <v-card-title class="font-weight-black text-center">Confirm Logout</v-card-title>
            <v-card-text class="text-center">Are you sure you want to log out?</v-card-text>
            <v-card-actions class="justify-center">
              <v-btn text style="background-color: white; color: #803d3b;" @click="confirmLogout">Yes</v-btn>
              <v-btn text style="background-color: #803d3b; color: white;" @click="cancelLogout">Cancel</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-app-bar>
    </div>

    <!-- Main Content -->
    <v-main class="custom-main">
      <v-container fluid class="main-container pa-8 rounded-lg">
        <!-- Dashboard Tab -->
        <v-row v-if="authStore.user?.email === 'admin@gmail.com' && activeTab === 'dashboard'">
          <v-col cols="12">
            <UserTable :userData="users" />
          </v-col>
        </v-row>

        <!-- Chats Tab -->
        <v-row v-else-if="authStore.user?.email !== 'admin@gmail.com' && activeTab === 'chats'">
          <v-col cols="12">
            <ChatBox />
          </v-col>
        </v-row>

       
      </v-container>
    </v-main>

    <!-- Floating Buttons -->
    <div class="floating-buttons">
      <!-- Dashboard button for Admin -->
      <v-btn
        v-if="authStore.user?.email === 'admin@gmail.com'"
        class="floating-btn"
        dark
        style="background-color: white; color: black;"
        elevation="15"
        @click="activeTab = 'dashboard'"
      >
        <v-icon left>mdi-view-dashboard</v-icon> Dashboard
      </v-btn>

      <!-- Messages button for non-admin -->
      <v-btn
        v-if="authStore.user?.email !== 'admin@gmail.com'"
        class="floating-btn"
        style="background-color: white; color: black;"
        dark
        elevation="15"
        @click="activeTab = 'chats'"
      >
        <v-icon left>mdi-chat</v-icon> Messages
      </v-btn>

    
    </div>
  </v-app>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import UserTable from "@/views/dashboard/UserTable.vue";
import ChatBox from "@/components/ChatBox.vue";

const users = ref([]);
const activeTab = ref(localStorage.getItem("activeTab") || "dashboard");
const logoutModal = ref(false);
const authStore = useAuthStore();

// Fetch user data
const fetchUsers = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/users/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });
    users.value = response.data.data.users.map((user) => ({
      id: user.id,
      username: user.name,
      email: user.email,
      status: "active",
    }));
  } catch (err) {
    console.error("Error fetching users:", err.message);
  }
};

// Logout modal handlers
const showLogoutConfirmation = () => (logoutModal.value = true);
const confirmLogout = () => {
  logoutModal.value = false;
  authStore.logout();
};
const cancelLogout = () => (logoutModal.value = false);

onMounted(() => {
  fetchUsers();
  // Default tab based on user type
  if (authStore.user?.email === "admin@gmail.com") {
    activeTab.value = "dashboard";
  } else {
    activeTab.value = "chats";
  }
});

watch(activeTab, (newTab) => {
  localStorage.setItem("activeTab", newTab);
});
</script>





<style scoped>
@import url('https://fonts.cdnfonts.com/css/unbounded');
.app-container {
  background-color: #803d3b;
  color: white;
}

.custom-main {
  padding-top: 64px;
}

.main-container {
  border-radius: 12px;
  color: black;
}

.floating-buttons {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  z-index: 1000;
}

.navbar {
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.7), 0px 4px 10px rgba(50, 50, 50, 0.5);
}

.title {
  font-family: 'Unbounded', Arial, sans-serif;
}

.floating-btn {
  border-radius: 50px;
  font-size: 16px;
  padding: 10px 20px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease;
  background-color: white;
}

.floating-btn:hover {
  transform: scale(1.1);
}

.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background-color: black;
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.7), 0px 4px 10px rgba(50, 50, 50, 0.5);
}

::v-deep(.v-overlay__scrim) {
  backdrop-filter: blur(50px) !important;
  background-color: rgba(0, 0, 0, 0.877) !important;
}
</style>
