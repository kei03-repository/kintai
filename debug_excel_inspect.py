from openpyxl import load_workbook
wb = load_workbook(r'C:\Users\20013\OneDrive\デスクトップ\開発App\業務進捗報告_島.xlsx')
sh = wb['入力用']
print('merged ranges containing row 21-26:')
for r in sh.merged_cells.ranges:
    if r.min_row <= 26 and r.max_row >= 21:
        print(str(r), 'top-left', sh.cell(r.min_row, r.min_col).coordinate)
print('\nrow 21 columns 8-24:')
for c in range(8, 25):
    cell = sh.cell(row=21, column=c)
    print(cell.coordinate, repr(cell.value), 'merged' if any(cell.coordinate in str(m) for m in sh.merged_cells.ranges) else '')
print('\nrow 23 columns 8-24:')
for c in range(8, 25):
    cell = sh.cell(row=23, column=c)
    print(cell.coordinate, repr(cell.value), 'merged' if any(cell.coordinate in str(m) for m in sh.merged_cells.ranges) else '')
print('\nrow 24 columns 8-24:')
for c in range(8, 25):
    cell = sh.cell(row=24, column=c)
    print(cell.coordinate, repr(cell.value), 'merged' if any(cell.coordinate in str(m) for m in sh.merged_cells.ranges) else '')
print('\nrow 23-24 merged status exact:')
for c in range(8, 25):
    coords = [sh.cell(row=r, column=c).coordinate for r in (23,24)]
    merged = [str(m) for m in sh.merged_cells.ranges if any(coord in str(m) for coord in coords)]
    if merged:
        print(c, coords, merged)
