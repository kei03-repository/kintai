export interface AttendanceCreateInput {
  date: string;
  category1?: string;
  category2?: string;
  start_time?: string;
  end_time?: string;
  break_minutes?: number;
  notes?: string;
}

export interface AttendanceData {
  id: number;
  date: string;
  category1?: string | null;
  category2?: string | null;
  start_time?: string | null;
  end_time?: string | null;
  break_minutes: number;
  notes?: string | null;
}
