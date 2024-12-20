<script setup>
import { defineProps } from "vue";


const props = defineProps({
  userData: {
    type: Array,
    required: true,
  },
});

const headers = [
  {
    title: "User",
    key: "username",
  },
  {
    title: "Email",
    key: "email",
  },
  {
    title: "Status",
    key: "status",
  },
];

const resolveUserStatusVariant = (stat) => {
  const statLowerCase = stat.toLowerCase();
  if (statLowerCase === "pending") return "warning";
  if (statLowerCase === "active") return "success";
  if (statLowerCase === "inactive") return "secondary";

  return "primary";
};
</script>

<template>
  <v-card class="table-card">
    <v-data-table
      :headers="headers"
      :items="userData"
      item-value="id"
      class=" custom-table"
    >
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

      <template #bottom />
    </v-data-table>
  </v-card>
</template>
<style scoped>
@import url('https://fonts.cdnfonts.com/css/unbounded');
@import url('https://fonts.cdnfonts.com/css/wix-madefor-display');
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
