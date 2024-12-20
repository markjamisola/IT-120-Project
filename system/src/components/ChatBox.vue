<template>
  <v-container>
    <v-row>
      <!-- Inbox (left sidebar) -->
      <v-col cols="12" md="4">
        <v-card class="inbox-card" elevation="15">
          <v-card-title class="inbox-title">
            <div>Available Users</div>
          </v-card-title>
          <v-list>
            <v-list-item-group v-if="filteredUsers.length > 0">
              <v-list-item
                v-for="user in filteredUsers"
                :key="user.id"
                class="user-item"
                @click="selectReceiver(user)"
              >
                <v-list-item-avatar>
                  <v-img :src="user.avatar" class="user-avatar" />
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title class="user-name">{{ user.name }}</v-list-item-title>
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
        <v-card v-if="selectedReceiver" class="chat-card" elevation="15">
          <v-card-title class="chat-header">
            <v-avatar class="receiver-avatar">
              <v-img :src="selectedReceiver.avatar" />
            </v-avatar>
            <div>
              <div class="receiver-name">{{ selectedReceiver.name }}</div>
              <div class="receiver-caption">Chat with {{ selectedReceiver.name }}</div>
            </div>
          </v-card-title>

          <v-card-subtitle>
            <v-scroll-y class="message-container">
              <v-list class="lista">
                      <v-list-item-group v-if="combinedMessages.length > 0">
                        <v-list-item v-for="message in combinedMessages" :key="message.id">
                          <v-list-item-content>
                            <div
                              class="message"
                              :class="{
                                'sent-message': message.isSentByMe,
                                'received-message': !message.isSentByMe,
                              }"
                            >
                              <div class="message-text">{{ message.content }}</div>
                              <span class="timestamp">{{ formatTimestamp(message.timestamp) }}</span>
                            </div>
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

          <!-- Message Input -->
          <v-card-actions class="input-container">
            <v-textarea
              v-model="newMessage"
              placeholder="Type your message..."
              rows="1"
              outlined
              dense
              class="message-input"
            />
            <v-btn @click="sendMessage" :disabled="!newMessage" class="send-button px-7" color="white">
              Send
            </v-btn>
          </v-card-actions>
        </v-card>

        <v-card v-else class="empty-chat-card">
          <v-card-title>
            <div class="empty-chat-title pt-9">Select a user to chat with</div>
          </v-card-title>
          <v-card-subtitle>
            <div class="empty-chat-caption">
              Click on a user from the Inbox to start a chat. Ensure that your secrets are safe with us.
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
      newMessage: "",
      messages: [],
      replies: [],
    };
  },
  created() {
    this.fetchUserData();
    this.fetchUsers();
    this.startPolling();
  },
  computed: {
    filteredUsers() {
      return this.users.filter((user) => user.id !== this.user.id);
    },
    combinedMessages() {
  const messages = [...this.messages, ...this.replies]
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
    .map((msg) => ({
      ...msg,
      isSentByMe: msg.sender_id === this.user.id,
    }));
  console.log("Combined Messages:", messages);
  return messages;
},

  },
  methods: {
    async fetchUserData() {
      try {
        const response = await axios.get("http://localhost:8000/api/me/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        this.user = response.data;
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
    async fetchUsers() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/users/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
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
      if (!this.selectedReceiver) return;
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/chat/api/messages/",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            params: {
              sender_id: this.user.id,
              receiver_id: this.selectedReceiver.id,
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
      if (!this.selectedReceiver) return;
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/chat/api/replies/",
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
    async sendMessage() {
      if (!this.selectedReceiver || !this.newMessage) return;

      const encryptedMessage = CryptoJS.AES.encrypt(
        this.newMessage,
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
        this.messages.push({
          ...messageData,
          id: response.data.id,
          content: this.newMessage, // Show plaintext immediately
        });
        this.newMessage = "";
      } catch (error) {
        console.error("Error sending message:", error);
      }
    },
    startPolling() {
      setInterval(() => {
        if (this.selectedReceiver) {
          this.fetchMessages();
          this.fetchReplies();
        }
      }, 1000); // Poll every 2 seconds
    },
    decryptMessage(encryptedContent) {
      try {
        const bytes = CryptoJS.AES.decrypt(encryptedContent, ENCRYPTION_KEY);
        return bytes.toString(CryptoJS.enc.Utf8);
      } catch (error) {
        console.error("Error decrypting message:", error);
        return "Decryption failed";
      }
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.cdnfonts.com/css/unbounded');
@import url('https://fonts.cdnfonts.com/css/wix-madefor-display');
.headline {
  font-size: 1.5em;
  font-weight: bold;
  font-family: "monospace";
}

.lista{
background-color: #000;
}

.caption {
  font-size: 0.9em;
  color: grey;
}

/* Inbox Styles */
.inbox-card {
  background-color: #000000;
  border-radius: 10px;
  overflow: hidden;
}

.inbox-title {
  font-size: 1.2em;
  font-weight: 600;
  background-color: #282828;
  color: white;
  padding: 10px;
  text-align: center;
  font-family: 'Unbounded', Arial, sans-serif;

}

.user-item {
  cursor: pointer;
  transition: background-color 0.3s;
  background-color: #000;
  font-family: 'Wix Madefor Display', sans-serif;  
}

.user-item:hover {
  background-color: #ffffff;
  color: #000;
}

.user-avatar {
  border-radius: 50%;
}

.user-name {
  font-weight: bold;
  font-size: 1.1em;
  text-align: center;
}

/* Chat Box Styles */
.chat-card {
  background-color: #000000;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
  font-family: 'Wix Madefor Display', sans-serif;  

}

.chat-header {
  background-color: #282828;
  color: white;
  padding: 15px;
  display: flex;
  align-items: center;
  font-family: 'Unbounded', Arial, sans-serif;
}

.receiver-avatar {
  margin-right: 10px;
}

.receiver-name {
  font-size: 1.5em;
  font-weight: bold;
}

.receiver-caption {
  font-size: 0.9em;
  color: #e0e0e0;
}

.message-container {
  flex-grow: 1;
  max-height: 500px;
  overflow-y: auto;
  padding: 10px;
  background-color: #000000;
  display: flex;
  flex-direction: column;
}

.message {
  display: inline-block;
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 15px;
  margin-bottom: 10px;
  position: relative;
  word-wrap: break-word;
}

.sent-message {
  background-color: #1976d2;
  color: white;
  align-self: flex-end; /* Aligns message to the right */
  text-align: right; /* Ensures text is aligned to the right */
  margin-left: auto; /* Pushes the message to the right */
  border-top-right-radius: 0; /* Adds some differentiation */
}

.received-message {
  background-color: #e0e0e0;
  color: black;
  align-self: flex-start; /* Aligns message to the left */
  text-align: left; /* Ensures text is aligned to the left */
  margin-right: auto; /* Pushes the message to the left */
  border-top-left-radius: 0; /* Adds some differentiation */
}

.message-text {
  font-size: 1em;
  line-height: 1.4;
  font-weight: bold;
}

.timestamp {
  font-size: 0.8em;
  color: rgb(0, 0, 0);
  display: block;
  margin-top: 5px;
  text-align: right;
}

/* Input Styles */
.input-container {

  background-color: #000000;
  display: flex;
  align-items: center;
}

.message-input {
  flex-grow: 1;
  margin-right: 20px;
  border-radius: 20px;
  background-color: #ffffff;
  border: 1px solid #ddd;
  color: black;
  margin-left: 30px;
  margin-bottom: 20px;
}

.send-button {
  border-radius: 20px;
  background-color: #803d3b;
  margin-right: 20px;
  font-weight: bold;
}

/* Empty Chat Styles */
.empty-chat-card {
  text-align: center;
  background-color: transparent;

  padding-bottom: 50px;
  border: none; /* Remove any border */
  box-shadow: none; /* Remove shadow */
}

.empty-chat-title {
  font-size: 1.2em;
  font-weight: bold;
  font-family: 'Unbounded', Arial, sans-serif;

}

.empty-chat-caption {
  font-size: 1em;
  color: rgb(255, 255, 255);
  font-family: 'Wix Madefor Display', sans-serif;  
}
</style>
