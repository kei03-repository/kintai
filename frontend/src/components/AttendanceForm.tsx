import { FormEvent, useState } from 'react';
import { AttendanceCreateInput } from '../types';
import { CATEGORY1_OPTIONS, CATEGORY2_OPTIONS } from '../constants/attendance';

interface AttendanceFormProps {
  onSaved: () => void;
}

const defaultForm: AttendanceCreateInput = {
  date: new Date().toISOString().slice(0, 10),
  category1: '',
  category2: '',
  start_time: '08:45',
  end_time: '17:45',
  break_minutes: 60,
  notes: '',
};

function AttendanceForm({ onSaved }: AttendanceFormProps) {
  const [form, setForm] = useState<AttendanceCreateInput>(defaultForm);
  const [status, setStatus] = useState<string | null>(null);

  const handleChange = (field: keyof AttendanceCreateInput, value: string | number) => {
    setForm({ ...form, [field]: value });
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const payload = { ...form, date: form.date };
    const response = await fetch('/api/attendances', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      setStatus('保存に失敗しました。');
      return;
    }
    setStatus('保存しました。');
    onSaved();
  };

  return (
    <section className="form-section">
      <h2>勤怠入力</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <label>
            日付:
            <input
              type="date"
              value={form.date}
              onChange={(event) => handleChange('date', event.target.value)}
              required
            />
          </label>
          <label>
            区分1:
            <select
              value={form.category1}
              onChange={(event) => handleChange('category1', event.target.value)}
            >
              <option value="">選択してください</option>
              {CATEGORY1_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {`${option.value}：${option.label}`}
                </option>
              ))}
            </select>
          </label>
          <label>
            区分2:
            <select
              value={form.category2}
              onChange={(event) => handleChange('category2', event.target.value)}
            >
              <option value="">選択してください</option>
              {CATEGORY2_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {`${option.value}：${option.label}`}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="form-row">
          <label>
            開始時間:
            <input
              className="time-input"
              type="time"
              value={form.start_time}
              onChange={(event) => handleChange('start_time', event.target.value)}
            />
          </label>
          <label>
            終了時間:
            <input
              className="time-input"
              type="time"
              value={form.end_time}
              onChange={(event) => handleChange('end_time', event.target.value)}
            />
          </label>
          <label>
            定時帯休憩時間:
            <input
              className="time-input"
              type="text"
              value="1:00"
              readOnly
              aria-readonly="true"
            />
          </label>
          <input
            type="hidden"
            value={form.break_minutes}
            readOnly
            aria-hidden="true"
          />
        </div>

        <div className="form-row full-width">
          <label>
            備考:
            <textarea
              value={form.notes}
              onChange={(event) => handleChange('notes', event.target.value)}
              rows={3}
            />
          </label>
        </div>

        <button type="submit">保存</button>
        {status && <div className="form-status">{status}</div>}
      </form>
    </section>
  );
}

export default AttendanceForm;
