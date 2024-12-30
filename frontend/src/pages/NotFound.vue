<template>
  <VSheet class="notfound d-flex align-center justify-center" height="100%">
    <VEmptyState headline="Whoops, 404" title="Page not found" text="The page you were looking for does not exist"
      icon="mdi-magnify" action-text="返回首页" @click:action="goToIndex()" />
  </VSheet>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToIndex = () => {
  router.push({ path: '/' })
}
</script>

<route lang="yaml">
meta:
  layout: users
</route>

<style scoped lang="scss">
.notfound {
  color: orange;
}
</style>
