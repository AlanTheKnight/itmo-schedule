<template>
  <div v-for="ev in events" class="card card-body mb-2 ps-4">
    <div
      class="position-absolute color-indicator"
      :class="['bg-' + (colors.get(ev.type) || 'light')]"
    ></div>
    <h3 class="fs-5">{{ ev.subject }}</h3>
    {{ ev.time_start }} - {{ ev.time_end }}
  </div>
</template>

<script setup lang="ts">
import { colors } from "@/utils/colors";
import { ITMOEvent } from "~/api/schedule";

interface Props {
  events: ITMOEvent[];
}

defineProps<Props>();
</script>

<style scoped>
.color-indicator {
  width: 0.5rem;
  height: 100%;
  top: 0;
  left: 0;
  border-radius: 0.25rem 0 0 0.25rem;
}

.bg-purple {
  background-color: #6f42c1;
}
</style>
