<script setup lang="ts">
import {
  ITMOEvent,
  ScheduleRequest,
  createScheduleRequest,
  transformSchedule,
  fetchSchedule,
  ScheduleJSON,
} from "@/api/schedule";

const data = reactive({
  username: "",
  password: "",
  date_start: "2023-09-04",
  date_end: "2023-10-01",
});

const errorText = ref<null | any>(null);

const scheduleRequest = ref<null | ScheduleRequest>(null);
const schedule = ref<null | Record<string, ITMOEvent[]>>(null);

const intervalId = ref<null | any>(null);

const refreshRequest = async () => {
  if (!scheduleRequest.value || !statusUnfinished.value) {
    if (scheduleRequest.value?.status === "status.Ready") {
      schedule.value = transformSchedule(scheduleRequest.value);
    }
    if (intervalId.value) clearInterval(intervalId.value);
    return;
  }

  const resp = await fetchSchedule(scheduleRequest.value.id, (error) => {
    errorText.value = error;
  });
  if (resp) scheduleRequest.value = resp;
};

const onSubmit = async () => {
  errorText.value = null;
  const resp = await createScheduleRequest(data, (error) => {
    errorText.value = error;
  });

  if (resp) {
    scheduleRequest.value = resp;
  }

  if (intervalId.value) clearInterval(intervalId.value);
  intervalId.value = setInterval(refreshRequest, 3000);
};

const statusUnfinished = computed(() => {
  return (
    scheduleRequest.value &&
    scheduleRequest.value.status !== "status.Ready" &&
    scheduleRequest.value.status !== "status.Failed"
  );
});
</script>

<template>
  <div class="container mt-5">
    <h1 class="mb-5">ITMO Schedule Exporter</h1>

    <div class="row d-flex">
      <div class="col-12 col-md-8">
        <div v-if="errorText || scheduleRequest?.error">
          <div class="alert alert-danger">
            <i class="bi bi-exclamation-circle me-2"></i
            >{{
              scheduleRequest?.error ||
              (errorText.data.error ? errorText.data.error : errorText)
            }}
          </div>
        </div>
        <div v-else-if="scheduleRequest !== null">
          <Loading :state="!statusUnfinished">
            <div v-if="scheduleRequest.status === 'status.Ready'">
              <div class="mb-3">
                <a
                  class="btn btn-outline-success"
                  :href="(scheduleRequest?.ics_file as string)"
                >
                  <i class="bi bi-file-earmark-arrow-down-fill me-2"></i>
                  Download .ics
                </a>
              </div>
              <ScheduleList v-if="schedule" :schedule="schedule" />
            </div>
          </Loading>
        </div>
        <div v-else>
          <div class="alert alert-light">
            <i class="bi bi-info-circle me-2"></i>
            Submit the form to export your schedule
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4">
        <div class="card card-body">
          <FormKit type="form" @submit="onSubmit">
            <div class="mb-3">
              <FormKit
                type="text"
                label="ISU login"
                v-model="data.username"
                validation="required"
                validation-visibility="blur"
              />
            </div>
            <div class="mb-3">
              <FormKit
                type="password"
                label="Password"
                v-model="data.password"
                validation="required"
                validation-visibility="blur"
              />
            </div>
            <div class="mb-3">
              <FormKit
                type="date"
                label="Start date"
                v-model="data.date_start"
                validation="required|date_after:2023-09-01"
                validation-visibility="blur"
              />
            </div>
            <div class="mb-3">
              <FormKit
                type="date"
                label="End date"
                v-model="data.date_end"
                validation="required|date_before:2023-12-24"
                validation-visibility="blur"
              />
            </div>
          </FormKit>
        </div>
      </div>
    </div>
  </div>
</template>
