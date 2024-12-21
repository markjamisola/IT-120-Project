<script setup>
import { defineProps, watch, computed } from "vue";
import { ref } from "vue";
import axios from "axios";

const props = defineProps({
  userData: {
    type: Array,
    required: true,
  },
});

// Filter out the user with the email "admin@gmail.com"
const filteredUserData = computed(() =>
  props.userData.filter((user) => user.email !== "admin@gmail.com")
);

// Total number of users excluding "admin@gmail.com"
const totalUsers = computed(() => filteredUserData.value.length);

// Table headers for the users table
const userHeaders = [
  { title: "ID", key: "id" },
  { title: "User", key: "username" },
  { title: "Email", key: "email" },
  { title: "Status", key: "status" },
];

// Log userData to verify the structure
watch(
  () => props.userData,
  (newUserData) => {
    console.log(newUserData); // Check the structure of userData
    if (newUserData.length > 0) {
      fetchEncryptedMessages();
    }
  },
  { immediate: true }
);

// Resolve status to chip color
const resolveUserStatusVariant = (stat) => {
  const statLowerCase = stat.toLowerCase();
  if (statLowerCase === "pending") return "warning";
  if (statLowerCase === "active") return "success";
  if (statLowerCase === "inactive") return "secondary";
  return "primary";
};

// Store messages
const messages = ref([]);

// Total number of messages
const totalMessages = computed(() => messages.value.length);

// Headers for the encrypted messages table
const messageHeaders = [
  { title: "ID", key: "id" },
  { title: "Sender", key: "sender" },
  { title: "Receiver", key: "receiver" },
  { title: "Content", key: "content" },
  { title: "Timestamp", key: "timestamp" },
];

// Fetch encrypted messages and map sender/receiver names
const fetchEncryptedMessages = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/chat/api/messages/", {
      headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` },
    });

    // Map messages with formatted timestamp
    messages.value = response.data.map((msg) => ({
      ...msg,
      timestamp: new Date(msg.timestamp).toLocaleString(),
    }));
  } catch (error) {
    console.error("Error fetching encrypted messages:", error);
  }
};
</script>

<template>
    <v-row class="statistics-section" align="center" justify="center">
    <!-- Welcome Message -->
    <v-col cols="12" class="d-flex justify-center mb-4">
      <h2 class="welcome-message">Welcome to Admin Dashboard</h2>
    </v-col>

    <v-col cols="12" md="4" class="d-flex justify-center">
      <!-- Total Users Card -->
      <v-card class="statistics-card square-card">
        <v-card-text class="d-flex flex-column justify-center align-center">
          <h3>Total Users</h3>
          <p>{{ totalUsers }}</p>
        </v-card-text>
      </v-card>
    </v-col>

    <v-col cols="12" md="4" class="d-flex justify-center">
      <!-- Total Messages Card -->
      <v-card class="statistics-card square-card">
        <v-card-text class="d-flex flex-column justify-center align-center">
          <h3>Total Messages</h3>
          <p>{{ totalMessages }}</p>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <!-- User Table -->
  <v-card class="table-card">
    <v-data-table
      :headers="userHeaders"
      :items="filteredUserData"
      item-value="id"
      class="custom-table"
    >
      <!-- User ID -->
      <template #item.id="{ item }">
        <span>{{ item.id }}</span>
      </template>

      <!-- User -->
      <template #item.username="{ item }">
        <div class="d-flex align-center" style="gap: 15px">
          <div class="d-flex flex-column">
            <h6 class="text-h6 font-weight-medium user-list-name">
              {{ item.username }}
            </h6>
          </div>
        </div>
      </template>

      <!-- Status -->
      <template #item.status="{ item }">
        <v-chip
          :color="resolveUserStatusVariant(item.status)"
          size="small"
          class="text-capitalize"
        >
          {{ item.status }}
        </v-chip>
      </template>
    </v-data-table>
  </v-card>

  <!-- Encrypted Messages Table -->
  <v-card class="table-card mt-4">
    <v-data-table
      :headers="messageHeaders"
      :items="messages"
      item-value="id"
      class="custom-table"
    >
      <!-- Encrypted Content -->
      <template #item.content="{ item }">
        <code>{{ item.content }}</code>
      </template>
    </v-data-table>
  </v-card>
</template>

<style scoped>
@import url('https://fonts.cdnfonts.com/css/unbounded');
@import url('https://fonts.cdnfonts.com/css/wix-madefor-display');

/* Statistics Section Styling */
.statistics-section {
  margin-bottom: 16px;
}

.statistics-card {
  background-color: #282828;
  color: white;
  border-radius: 12px;
}

.statistics-card h3 {
  font-family: 'Wix Madefor Display', sans-serif;
  font-weight: bold;
}

.statistics-card p {
  font-size: 24px;
  font-family: 'Unbounded', Arial, sans-serif;
}

.square-card {
  width: 200px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

/* Welcome message styling */
.welcome-message {
  font-family: 'Wix Madefor Display', sans-serif;
  color: white;
  font-weight: bold;
  font-size: 32px;
  text-align: center;
  margin-top: 0;
}

.square-card {
  width: 200px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.table-card {
  background-color: black; /* Card background color */
  border-radius: 12px; /* Rounded corners */
  overflow: hidden; /* Ensure rounded corners are applied properly */
}

::v-deep(.custom-table) {
  background-color: black; /* Table background color */
  color: white; /* Text color */
}

::v-deep(.custom-table thead th) {
  background-color: #282828; /* Header background color */
  color: rgb(255, 255, 255); /* Header text color */
  font-weight: bold;
  font-family: 'Unbounded', Arial, sans-serif;
  font-size: 18px; /* Adjust font size as needed */
}

::v-deep(.custom-table thead th:hover) {
  color: rgb(0, 0, 0); /* Header text color */
  font-weight: bold;
}

::v-deep(.custom-table tbody tr) {
  border-bottom: 1px solid #444; /* Row border */
  font-family: 'Wix Madefor Display', sans-serif;
}

::v-deep(.custom-table tbody tr:hover) {
  background-color: #333; /* Highlight on hover */
}
</style>
