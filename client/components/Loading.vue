<script setup lang="ts">
interface Props {
  state: boolean;
}
defineProps<Props>();
</script>

<template>
  <div v-if="state">
    <slot />
  </div>
  <div v-else class="text-center">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>
