<template>
  <v-container>
    <v-row>
      <!-- Inbox (left sidebar) -->
      <v-col cols="12" md="4">
        <v-card class="mb-3" elevation="2">
          <v-card-title>
            <div class="headline">Available Users</div>
          </v-card-title>
          <v-list>
            <v-list-item-group v-if="filteredUsers.length > 0">
              <v-list-item
                v-for="user in filteredUsers"
                :key="user.id"
                @click="selectReceiver(user)"
              >
                <v-list-item-avatar>
                  <v-img :src="user.avatar" />
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>{{ user.name }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
            <v-list-item v-else>
              <v-list-item-content>
                <v-list-item-title>No conversations available...</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- Chat Box (right section) -->
      <v-col cols="12" md="8">
        <v-card v-if="selectedReceiver" class="pa-3" elevation="2">
          <v-card-title>
            <v-avatar class="mr-3">
              <v-img :src="selectedReceiver.avatar" />
            </v-avatar>
            <div>
              <div class="caption">Chatting with: {{ selectedReceiver.name }}</div>
            </div>
          </v-card-title>

          <v-card-subtitle>
            <v-scroll-y class="message-list">
              <v-list>
                <v-list-item-group v-if="combinedMessages.length > 0">
                  <v-list-item v-for="message in combinedMessages" :key="message.id">
                    <v-list-item-content>
                      <v-list-item-title>
                        <v-card
                          class="pa-3 mb-3"
                          :class="{
                            'sent-message': message.isSentByMe,
                            'received-message': !message.isSentByMe,
                          }"
                        >
                          <h4>{{ message.content }}</h4>
                        </v-card>
                      </v-list-item-title>
                      <span class="mx-5">{{ formatTimestamp(message.timestamp) }}</span>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
                <v-list-item v-else>
                  <v-list-item-content>
                    <v-list-item-title>No messages yet...</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-scroll-y>
          </v-card-subtitle>

          <v-card-actions>
            <v-text-field
              v-model="replyMessage"
              label="Enter your reply"
              outlined
            ></v-text-field>
            <v-btn color="primary" @click="sendReply">Reply</v-btn>
          </v-card-actions>
        </v-card>

        <v-card v-else class="pa-3" elevation="2">
          <v-card-title>
            <div class="headline">Select a user to chat with</div>
          </v-card-title>
          <v-card-subtitle>
            <div class="caption">
              Click on a user from the inbox to start a chat.
            </div>
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import CryptoJS from "crypto-js";

const ENCRYPTION_KEY = "3aIYac2hijTnCvnQ_cYTOEiCReFBHyI3APLJxi9HAfY=";

export default {
  data() {
    return {
      user: {},
      users: [],
      selectedReceiver: null,
      messages: [],
      replies: [],
      replyMessage: "", // Input for reply
    };
  },
  created() {
    this.fetchUserData();
    this.fetchUsers();
    this.startMessagePolling();
  },
  computed: {
    filteredUsers() {
      return this.users.filter((user) => user.id !== this.user.id);
    },
    combinedMessages() {
      return [...this.messages, ...this.replies]
        .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
        .map((msg) => ({
          ...msg,
          isSentByMe: msg.sender_id === this.user.id,
        }));
    },
  },
  methods: {
    async fetchUserData() {
      try {
        const response = await axios.get("http://localhost:8000/api/me/", {
          headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` },
        });
        this.user = response.data;
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
    async fetchUsers() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/users/", {
          headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` },
        });
        this.users = response.data.data.users || [];
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    selectReceiver(user) {
      this.selectedReceiver = user;
      this.fetchMessages();
      this.fetchReplies();
    },
    async fetchMessages() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/chat/api/messages/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            params: {
              receiver_id: this.selectedReceiver.id,
              sender_id: this.user.id,
            },
          }
        );
        this.messages = response.data.map((msg) => ({
          ...msg,
          content: this.decryptMessage(msg.content),
        }));
      } catch (error) {
        console.error("Error fetching messages:", error);
      }
    },
    async fetchReplies() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/chat/api/conversation-messages/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            params: {
              sender_id: this.selectedReceiver.id,
              receiver_id: this.user.id,
            },
          }
        );
        this.replies = response.data.map((reply) => ({
          ...reply,
          content: this.decryptMessage(reply.content),
        }));
      } catch (error) {
        console.error("Error fetching replies:", error);
      }
    },
    async sendReply() {
      if (!this.selectedReceiver || !this.replyMessage) return;

      // Encrypt the reply message
      const encryptedMessage = CryptoJS.AES.encrypt(
        this.replyMessage,
        ENCRYPTION_KEY
      ).toString();

      const messageData = {
        sender: this.user.id,
        receiver: this.selectedReceiver.id,
        content: encryptedMessage,
        timestamp: new Date().toISOString(),
      };

      try {
        const response = await axios.post(
          "http://localhost:8000/chat/api/messages/",
          messageData,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        // Update the messages array locally with decrypted message for display
        this.messages.push({
          id: response.data.id,
          content: this.replyMessage,
          sender_name: this.user.name,
          timestamp: messageData.timestamp,
        });

        this.replyMessage = ""; // Clear the input
      } catch (error) {
        console.error("Error sending reply:", error);
      }
    },
    startMessagePolling() {
      setInterval(() => {
        if (this.selectedReceiver) {
          this.fetchMessages();
          this.fetchReplies();
        }
      }, 1000);
    },
    decryptMessage(encryptedContent) {
  try {
    // Attempt to decrypt the message
    const bytes = CryptoJS.AES.decrypt(encryptedContent, ENCRYPTION_KEY);
    const decryptedMessage = bytes.toString(CryptoJS.enc.Utf8);

    // Check if decryption was successful
    if (!decryptedMessage) throw new Error("Decryption returned an empty string");

    return decryptedMessage;
  } catch (error) {
    console.error("Error decrypting message:", error);

    // Return a fallback or placeholder for decryption failure
    return "[Decryption failed: Invalid or corrupted content]";
  }
}
,
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
  },
};
</script>




<style scoped>
.headline {
  font-size: 1.5em;
  font-weight: bold;
  font-family: "monospace";
}

.caption {
  font-size: 0.9em;
  color: grey;
}

.selected-card {
  background-color: #f0f0f0;
  border: 1px solid #1976d2;
  color: #151515;
}

.v-list-item {
  cursor: pointer;
}

.v-card-actions {
  display: flex;
  align-items: center;
}

.v-textarea {
  flex-grow: 1;
  margin-right: 10px;
}

.v-btn {
  align-self: flex-start;
}
.message-list, .reply-list {
  max-height: 100px; /* Adjust height as needed */
  overflow-y: auto;
}
</style>
