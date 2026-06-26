export const CATEGORY1_OPTIONS: ReadonlyArray<{ value: string; label: string }> = [
  { value: '1', label: '出勤' },
  { value: '2', label: '欠勤' },
  { value: '3', label: '有給休暇(全日)' },
  { value: '4', label: '有給休暇(前半)' },
  { value: '5', label: '休日出勤' },
  { value: '6', label: '法定休日出勤' },
  { value: '7', label: '特別休暇' },
  { value: '8', label: '休業' },
  { value: '9', label: '有給休暇（後半）' },
];

export const CATEGORY2_OPTIONS: ReadonlyArray<{ value: string; label: string }> = [
  { value: '1', label: '遅刻' },
  { value: '2', label: '早退' },
  { value: '3', label: '遅刻＋早退' },
  { value: '4', label: '休業遅刻' },
  { value: '5', label: '休業早退' },
  { value: '6', label: '休業遅刻＋休業早退' },
];

export const CATEGORY1_LABELS: Record<string, string> = Object.fromEntries(
  CATEGORY1_OPTIONS.map((option) => [option.value, option.label]),
);

export const CATEGORY2_LABELS: Record<string, string> = Object.fromEntries(
  CATEGORY2_OPTIONS.map((option) => [option.value, option.label]),
);
