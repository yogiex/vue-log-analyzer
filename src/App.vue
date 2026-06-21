<template>
  <v-app>
    <router-view v-slot="{ Component, route }">
      <v-slide-x-reverse-transition mode="out-in">
        <component :is="Component" :key="route.path" />
      </v-slide-x-reverse-transition>
    </router-view>
  </v-app>
</template>
