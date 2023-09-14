<template>
  <div v-for="(events, date) in schedule">
    <h2 class="fs-4 mt-4 mb-2">
      {{
        new Date(date).toLocaleDateString(undefined, {
          weekday: "long",
          month: "short",
          day: "numeric",
        })
      }}
    </h2>
    <DayEventsCard :events="events" />
  </div>
</template>

<script setup lang="ts">
import { ITMOEvent } from "~/api/schedule";

interface Props {
  schedule: Record<string, ITMOEvent[]>;
}

defineProps<Props>();
</script>
