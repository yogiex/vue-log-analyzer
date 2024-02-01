<template>
<v-card
    flat
    title="User Filter"
  >
    <template v-slot:text>
      <v-text-field
        v-model="search"
        label="Search"
        prepend-inner-icon="mdi-magnify"
        single-line
        variant="outlined"
        hide-details
      ></v-text-field>
    </template>

    <v-data-table
      :headers="headers"
      :items="desserts"
      :search="search"
    ></v-data-table>
  </v-card>
</template>

<script>
let jsonData = []
// Function to generate a random public IP address
const generatePublicIp = () => `203.0.113.${Math.floor(Math.random() * 256)}`;

// Function to generate a unique user agent
const generateUserAgent = () => {
  const browsers = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera'];
  const randomBrowser = browsers[Math.floor(Math.random() * browsers.length)];
  const version = Math.floor(Math.random() * 50) + 50; // Random version between 50 and 100
  return `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ${randomBrowser}/${version}.0 Safari/537.3`;
};

// Generate 10 data entries
for (let i = 1; i <= 10; i++) {
  jsonData.push({
    name: `student student ${i < 10 ? '0' : ''}${i}`,
    first_ip: generatePublicIp(),
    last_ip: generatePublicIp(),
    last_access: `2024-01-31T16:${i < 10 ? '0' : ''}${i}:22:10Z`,
    user_agent: generateUserAgent(),
    status: 500
  });
}
console.log(jsonData)
export default {
    name: 'UsersViews',
    data () {
      return {
        search: '',
        headers: [
          {
            align: 'start',
            key: 'name',
            sortable: false,
            title: 'Username',
          },
          { key: 'first_ip', title: 'First IP' },
          { key: 'last_ip', title: 'Last IP' },
          { key: 'last_access', title: 'Last Access' },
          { key: 'user_agent', title: 'User-Agent' },
          { key: 'status', title: 'Status' },
        ],
        desserts: jsonData,
      }
    },
}

</script>