import { AttendanceData } from '../types';
import { CATEGORY1_LABELS, CATEGORY2_LABELS } from '../constants/attendance';

interface MonthlyListProps {
  attendances: AttendanceData[];
}

function MonthlyList({ attendances }: MonthlyListProps) {
  return (
    <section className="list-section">
      <h2>月ごとの勤怠一覧</h2>
      {attendances.length === 0 ? (
        <p>データがありません。日付と勤怠を入力してください。</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>日付</th>
              <th>区分1</th>
              <th>区分2</th>
              <th>開始</th>
              <th>終了</th>
              <th>休憩(分)</th>
              <th>備考</th>
            </tr>
          </thead>
          <tbody>
            {attendances.map((attendance) => (
              <tr key={attendance.id}>
                <td data-label="日付">{attendance.date}</td>
                <td data-label="区分1">
                  {attendance.category1 ? `${attendance.category1}: ${CATEGORY1_LABELS[attendance.category1] ?? attendance.category1}` : ''}
                </td>
                <td data-label="区分2">
                  {attendance.category2 ? `${attendance.category2}: ${CATEGORY2_LABELS[attendance.category2] ?? attendance.category2}` : ''}
                </td>
                <td data-label="開始">{attendance.start_time ?? ''}</td>
                <td data-label="終了">{attendance.end_time ?? ''}</td>
                <td data-label="休憩(分)">{attendance.break_minutes}</td>
                <td data-label="備考">{attendance.notes ?? ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}

export default MonthlyList;
