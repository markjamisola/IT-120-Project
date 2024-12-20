<script setup>
import { defineProps, watch } from "vue";
import { ref } from "vue";
import axios from "axios";

const props = defineProps({
  userData: {
    type: Array,
    required: true,
  },
});

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
  <!-- User Table -->
  <v-card>
    <v-data-table
      :headers="userHeaders"
      :items="userData"
      item-value="id"
    >
      <!-- User ID -->
      <template #item.id="{ item }">
        <span>{{ item.id }}</span> <!-- Ensure this is rendering the ID correctly -->
      </template>

      <!-- User -->
      <template #item.username="{ item }">
        <div class="d-flex align-center" style="gap: 15px">
          <v-avatar size="34" :variant="!item.avatar ? 'tonal' : undefined">
            <v-img v-if="item.avatar" :src="item.avatar" />
          </v-avatar>
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
  <v-card class="mt-4">
    <v-data-table
      :headers="messageHeaders"
      :items="messages"
      item-value="id"
      class="text-no-wrap"
    >
      <!-- Encrypted Content -->
      <template #item.content="{ item }">
        <code>{{ item.content }}</code>
      </template>
    </v-data-table>
  </v-card>
</template>
