<template>
  <v-app>
    <v-main>
      <VSonner position="top-center" expand />
      <router-view />
    </v-main>

    <!-- <AppFooter /> -->
  </v-app>
</template>

<script setup>
import { VSonner } from 'vuetify-sonner'
</script>
