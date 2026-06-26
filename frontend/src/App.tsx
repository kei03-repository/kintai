import { useEffect, useState } from 'react';
import AttendanceForm from './components/AttendanceForm';
import MonthlyList from './components/MonthlyList';
import { AttendanceData } from './types';

const today = new Date();

function App() {
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);
  const [attendances, setAttendances] = useState<AttendanceData[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  const loadAttendances = async () => {
    const response = await fetch(`/api/attendances?year=${year}&month=${month}`);
    if (!response.ok) {
      setMessage('勤怠一覧の取得に失敗しました。');
      return;
    }
    setAttendances(await response.json());
  };

  useEffect(() => {
    loadAttendances();
  }, [year, month]);

  const handleSaved = async () => {
    setMessage('保存しました。一覧を更新します。');
    await loadAttendances();
  };

  const handleExport = async () => {
    const response = await fetch(`/api/attendances/export?year=${year}&month=${month}`, {
      method: 'POST',
    });
    if (!response.ok) {
      setMessage('Excel の出力に失敗しました。');
      return;
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${month}月_業務進捗報告_島.xlsx`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    setMessage('Excel をダウンロードしました。');
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>勤怠管理アプリ</h1>
      </header>

      <section className="controls">
        <label>
          年:
          <input
            type="number"
            value={year}
            min={2000}
            onChange={(event) => setYear(Number(event.target.value))}
          />
        </label>
        <label>
          月:
          <input
            type="number"
            value={month}
            min={1}
            max={12}
            onChange={(event) => setMonth(Number(event.target.value))}
          />
        </label>
        <button type="button" onClick={loadAttendances}>
          月一覧更新
        </button>
        <button type="button" onClick={handleExport}>
          Excel 出力
        </button>
      </section>

      {message && <div className="message">{message}</div>}

      <AttendanceForm onSaved={handleSaved} />

      <MonthlyList attendances={attendances} />
    </div>
  );
}

export default App;
