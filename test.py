import py_compile
for f in ['att_db.py','attendance_sheet.py','main_attendance.py']:
    py_compile.compile(f, doraise=True)
print('OK')
