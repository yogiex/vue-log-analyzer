<template>
  <v-row>
    <v-col cols="12" md="6">
      <v-card title="System Information" variant="tonal">
        <v-list>
          <v-list-item title="Version" subtitle="1.0.0" />
          <v-list-item title="Status" subtitle="Operational">
            <template #append>
              <v-chip color="success" size="small">Active</v-chip>
            </template>
          </v-list-item>
          <v-list-item title="Last Backup" subtitle="2026-06-21 02:00 AM" />
          <v-list-item title="Uptime" subtitle="14 days 6 hours" />
        </v-list>
      </v-card>
    </v-col>
    <v-col cols="12" md="6">
      <v-card title="Configuration" variant="tonal">
        <v-list>
          <v-list-item title="Auto Sync" subtitle="Enabled">
            <template #append>
              <v-switch model-value="true" hide-details density="compact" />
            </template>
          </v-list-item>
          <v-list-item title="Notification" subtitle="Email alerts">
            <template #append>
              <v-switch model-value="true" hide-details density="compact" />
            </template>
          </v-list-item>
          <v-list-item title="Log Retention" subtitle="90 days" />
          <v-list-item title="Data Refresh" subtitle="Every 5 minutes" />
        </v-list>
      </v-card>
    </v-col>
  </v-row>
</template>
