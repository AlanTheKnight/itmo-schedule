export interface ITMOEvent {
  date: string;
  pair_id: number;
  subject: string;
  subject_id: number;
  note: string | null;
  type: string;
  time_start: string;
  time_end: string;
  teacher_id: number;
  teacher_name: string;
  room: string;
  building: string;
  format: string;
  work_type: string;
  work_type_id: number;
  group: string;
  flow_type_id: number;
  flow_id: number;
  zoom_url: string | null;
  zoom_password: string | null;
  zoom_info: string | null;
  bld_id: number;
  format_id: number;
  main_bld_id: number;
}

export interface ScheduleJSON {
  events: ITMOEvent[];
}

export interface ScheduleRequest {
  id: number;
  schedule_json: string;
  ics_file: null | string;
  generated_at: string;
  status:
    | "status.Queued"
    | "status.InProgress"
    | "status.Ready"
    | "status.Failed";
  error: null | string;
}

interface IGetSchedule {
  username: string;
  password: string;
  date_start: string;
  date_end: string;
}

const defaultHeaders = {
  "Content-Type": "application/json",
  "X-CSRFToken": (document.cookie.match(/csrftoken=([^ ;]+)/) as string[])[1],
};

export const createScheduleRequest = async (
  data: IGetSchedule,
  errorCallback?: (arg0: any) => void
) => {
  return await $fetch<ScheduleRequest>("/api/schedule/create", {
    method: "POST",
    body: data,
    headers: defaultHeaders,
  }).catch((err) => {
    errorCallback && errorCallback(err);
  });
};

export const fetchSchedule = async (
  pk: number,
  errorCallback?: (arg0: any) => void
) => {
  return await $fetch<ScheduleRequest>(`/api/schedule/${pk}`, {
    method: "GET",
    headers: defaultHeaders,
  }).catch((err) => {
    errorCallback && errorCallback(err);
  });
};

export const transformSchedule = (scheduleReq: ScheduleRequest) => {
  let schedule = (JSON.parse(scheduleReq.schedule_json) as ScheduleJSON).events;

  return schedule.reduce((acc, event) => {
    const date = event.date;
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(event);
    return acc;
  }, {} as Record<string, ITMOEvent[]>);
};
