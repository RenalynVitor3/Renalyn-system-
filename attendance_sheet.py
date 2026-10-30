import re
from datetime import datetime, time

import mysql.connector

import att_db

ARRIVAL_CUTOFF = time(7, 30)


def ask_text(msg):
    while True:
        v = input(msg).strip()
        if v == "":
            print("  * Hindi puwede blangko.")
            continue
        return v


def ask_clock_time(label):
    print(f"  [{label}] ENTER kung ngayon na, o ilagay ang HH:MM (24 oras)")
    a = input("    >> ").strip()
    if a == "":
        return datetime.now().strftime("%H:%M")
    if re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", a):
        return a
    print("  * Mali ang format.")
    return ask_clock_time(label)


def show_attendance_profile(s):
    print("\n" + "="*42)
    print(f"  STUDENT ID : {s['student_id']}")
    print("="*42)
    print(f"  Buong Pangalan : {s['full_name']}")
    if s.get('lrn'):
        print(f"  LRN            : {s['lrn']}")
    print(f"  Baitang/Seksyon: {s['grade_level']} - {s['section']}")
    if s.get('date_added'):
        print(f"  Idinagdag noong : {s['date_added']}")
    print("="*42)


def show_attendance_log(r):
    print("\n" + "="*42)
    print(f"  STUDENT ID : {r['student_id']}")
    print("="*42)
    print(f"  Buong Pangalan : {r['full_name']}")
    print(f"  Baitang/Seksyon: {r['grade_level']} - {r['section']}")
    print(f"  Petsa          : {r['att_date']}")
    print(f"  Time In        : {r['time_in'] or '---'}")
    print(f"  Time Out       : {r['time_out'] or '--- HINDI PA NAG-TIME OUT ---'}")
    print(f"  Status         : {r['status']}")
    if r.get('remarks'):
        print(f"  Tala           : {r['remarks']}")
    print("="*42)


def enroll_learner():
    print("\n--- MAGDAGDAG NG ESTUDYANTE SA MASTERLIST ---")
    sid = ask_text("  Student ID: ").upper()
    try:
        exist = att_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if exist:
        print("  [PAALALA] Mayroon nang estudyante na may ganitong Student ID.")
        show_attendance_profile(exist)
        return
    lrn = input("  LRN (opsyonal): ").strip() or None
    name = ask_text("  Buong Pangalan (Apelyido, Pangalan): ")
    gl = ask_text("  Baitang (hal. Grade 7): ")
    sec = ask_text("  Seksyon (hal. Rizal): ")
    try:
        att_db.add_student(sid, lrn, name, gl, sec)
        print("\n  [TAPOS NA] Naidagdag na ang estudyante sa masterlist.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def show_enrolled_learners():
    try:
        log_rows = att_db.list_students()
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not log_rows:
        print("\n  Wala pang estudyante sa masterlist.")
        return
    print("\n--- MASTERLIST NG MGA ESTUDYANTE ---")
    for r in log_rows:
        lrn_txt = f" | LRN:{r['lrn']}" if r.get('lrn') else ""
        print(f"  [{r['student_id']}] {r['full_name']} | {r['grade_level']} - {r['section']}{lrn_txt}")


def unenroll_learner():
    sid = ask_text("  Student ID na tatanggalin: ").upper()
    try:
        s = att_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not s:
        print("  [WALA] Hindi matagpuan ang estudyante sa masterlist.")
        return
    show_attendance_profile(s)
    konf = input("  Sigurado ka bang tanggalin ito sa masterlist? (oo/hindi): ").strip().lower()
    if konf not in ("oo", "o", "yes", "y"):
        print("  Kinansela.")
        return
    try:
        ok = att_db.delete_student(sid)
        if ok:
            print("  [TINANGGAL] Natanggal na ang estudyante sa masterlist.")
        else:
            print("  [MALI] Hindi nagtagumpay ang pagtanggal.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def log_arrival():
    print("\n--- TIME IN NG ESTUDYANTE ---")
    sid = ask_text("  Student ID: ").upper()
    try:
        s = att_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not s:
        print("  [WALA] Hindi pa naka-register ang estudyante sa masterlist.")
        print("  Paki-add muna sa [5] I-add ang Estudyante sa Masterlist.")
        return
    show_attendance_profile(s)
    today = datetime.now().date()
    try:
        open_rec = att_db.get_open_attendance(sid, today)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if open_rec:
        print("\n  [PAALALA] May TIME IN na siya ngayon at HINDI PA NAG-TIME OUT.")
        show_attendance_log(open_rec)
        return
    tin = ask_clock_time("Oras ng Time In")
    try:
        t_in_obj = datetime.strptime(tin, "%H:%M").time()
    except ValueError:
        t_in_obj = datetime.now().time()
    if t_in_obj > ARRIVAL_CUTOFF:
        status = "LATE"
        print("  [PAALALA] Lampas na sa 07:30 AM - STATUS: LATE")
    else:
        status = "PRESENT"
    try:
        att_db.time_in(sid, s['full_name'], s['grade_level'], s['section'], today, tin, status, None)
        print("\n  [TAPOS NA] Na-time in na ang estudyante.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def log_departure():
    print("\n--- TIME OUT NG ESTUDYANTE ---")
    sid = ask_text("  Student ID: ").upper()
    try:
        s = att_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not s:
        print("  [WALA] Hindi pa naka-register ang estudyante sa masterlist.")
        print("  Paki-add muna sa [5] I-add ang Estudyante sa Masterlist.")
        return
    today = datetime.now().date()
    try:
        open_rec = att_db.get_open_attendance(sid, today)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not open_rec:
        print("  [PAALALA] Wala siyang TIME IN ngayong araw o naka-time out na siya.")
        try:
            log_rows = att_db.get_attendance_by_student(sid)
            if log_rows:
                show_attendance_log(log_rows[0])
            else:
                show_attendance_profile(s)
        except mysql.connector.Error:
            show_attendance_profile(s)
        return
    show_attendance_log(open_rec)
    tout = ask_clock_time("Oras ng Time Out")
    try:
        ok = att_db.time_out(sid, today, tout)
        if ok:
            print("\n  [TAPOS NA] Na-time out na ang estudyante.")
        else:
            print("  [MALI] Hindi nagtagumpay ang Time Out.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def show_daily_roll():
    today = datetime.now().date()
    try:
        log_rows = att_db.get_attendance_by_date(today)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not log_rows:
        print("\n  Wala pang Time In sa araw na ito.")
        return
    print(f"\n--- ATTENDANCE NGAYONG ARAW ({today}) ---")
    for r in log_rows:
        tout = r['time_out'] or 'HINDI PA NAG-TIME OUT'
        print(f"  [{r['student_id']}] {r['full_name']} | {r['grade_level']} - {r['section']} | In:{r['time_in']} | Out:{tout} | {r['status']}")


def lookup_learner():
    sid = ask_text("  Student ID: ").upper()
    try:
        s = att_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not s:
        print("  [WALA] Hindi matagpuan ang estudyante sa masterlist.")
        return
    show_attendance_profile(s)
    try:
        log_rows = att_db.get_attendance_by_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not log_rows:
        print("\n  Wala pang attendance record ang estudyante na ito.")
        return
    print("\n--- MGA RECORD NG ATTENDANCE ---")
    for r in log_rows:
        tout = r['time_out'] or 'HINDI PA NAG-TIME OUT'
        print(f"  {r['att_date']} | In:{r['time_in']} | Out:{tout} | {r['status']}")
