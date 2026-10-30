import att_db
import attendance_sheet


def att_menu():
    print("\n" + "="*48)
    print("           ATTENDANCE SYSTEM - PAARALAN")
    print("="*48)
    print("  [1] Time In ng Estudyante")
    print("  [2] Time Out ng Estudyante")
    print("  [3] Tingnan ang Attendance Ngayon")
    print("  [4] Hanapin ang Record ng Estudyante")
    print("  [5] I-add ang Estudyante sa Masterlist")
    print("  [6] Tingnan ang Masterlist ng mga Estudyante")
    print("  [7] Tanggalin ang Estudyante sa Masterlist")
    print("  [0] Lumabas")
    print("="*48)


def att_cli():
    ok, msg = att_db.test_connection()
    print(f"\n  {msg}")
    if not ok:
        print("  Paki-import muna ang 'schema_attendance.sql' sa XAMPP/MySQL.")
        return
    while True:
        att_menu()
        ch = input("\n  Ano'ng aksyon ang gagawin? : ").strip()
        if ch == "1":
            attendance_sheet.log_arrival()
        elif ch == "2":
            attendance_sheet.log_departure()
        elif ch == "3":
            attendance_sheet.show_daily_roll()
        elif ch == "4":
            attendance_sheet.lookup_learner()
        elif ch == "5":
            attendance_sheet.enroll_learner()
        elif ch == "6":
            attendance_sheet.show_enrolled_learners()
        elif ch == "7":
            attendance_sheet.unenroll_learner()
        elif ch == "0":
            print("\n  Sige, paalam!")
            break
        else:
            print("\n  * Hindi tamang pagpili.")


if __name__ == "__main__":
    att_cli()
