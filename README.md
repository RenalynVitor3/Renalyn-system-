# School Attendance System

Kini nga sistema maoy talaan sa pagpasok ug paggawas sa mga estudyante. Matag
adlaw, mailhan kung **PRESENT** o **LATE** ang estudyante, ug makita ang tibuok
nga attendance sa maong adlaw. Naa pud kini masterlist sa mga estudyante.

## Unsa ang kinahanglan

- **Python 3.8 o mas bag-o**
- **XAMPP** (MySQL/MariaDB)
- **mysql-connector-python**

## 1) I-install ang MySQL connector

```powershell
pip install mysql-connector-python
```

## 2) Sugdi ang XAMPP

1. Ablihi ang **XAMPP Control Panel**.
2. Pindota ang **Start** tapad sa **MySQL**.
3. Siguroha nga **green** ang kolor sa MySQL.

## 3) I-import ang database

1. Ablihi ang `http://localhost/phpmyadmin`.
2. Pindota ang **Import** tab.
3. Pilia ang `schema_attendance.sql` (naa sa sama nga folder).
4. Pindota ang **Go** o **Import**.
5. Siguroha nga makita ang `school_attendance_db` sa lista sa wala.

## 4) Koneksyon sa database

| Variable | Default |
| --- | --- |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `3306` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | *(walay password)* |
| `DB_NAME` | `school_attendance_db` |

Kung lahi ang setup:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = ""
$env:DB_NAME = "school_attendance_db"
```

## 5) Padagana ang sistema

```powershell
cd "C:\Users\suete\Documents\system for sale\renalyn=school attendance_system"
python main_attendance.py
```

> Kung ibalhin ang folder sa lain nga computer, ilisi ang `cd` path sa
> aktwal nga lokasyon sa folder.


Dapat makita nimo ang **"Koneksyon sa School Attendance database ay OK na."**

## Mga file

| File | Tumong |
| --- | --- |
| `schema_attendance.sql` | Naghimo sa `students` ug `attendance` |
| `att_db.py` | SQL para sa masterlist ug attendance |
| `attendance_sheet.py` | Flow sa time in/out, pangita, ug listahan |
| `main_attendance.py` | Ang CLI menu |
| `test.py` | Pagsusi kung walay syntax error |

## Menu

| Numero | Aksyon |
| --- | --- |
| `1` | Time in sa estudyante |
| `2` | Time out sa estudyante |
| `3` | Tan-awa ang attendance karon |
| `4` | Pangitaa ang rekord sa estudyante |
| `5` | Pagdugang og estudyante sa masterlist |
| `6` | Tan-awa ang masterlist |
| `7` | Papasa ang estudyante sa masterlist |
| `0` | Gula |

## Unsaon ang time in ug time out

1. Pagdugang una og estudyante sa masterlist gamit ang `5`.
2. Pindota ang `1`, i-type ang **Student ID**.
3. Kung **ENTER** ra ang ibutang sa oras, gamiton ang karon nga oras. Mahimo
   pud mag-type og `HH:MM` (24-oras), pananglitan `07:15`.
4. Ang **07:30** maoy cutoff. Kung human sa 07:30, **LATE** ang status; kung
   dili, **PRESENT**.
5. Pindota ang `2` para sa time out. Kinahanglan naay time in sa maong adlaw.

## Importante nga lagda

- Dili makahimo og **duha ka time in** sa parehas nga adlaw ang usa ka estudyante.
- Dili makahimo og time out kung wala pay time in.
- Ang pagpapas sa estudyante sa masterlist dili automatic nga mopapas sa iyang
  mga attendance record.

## Giunsa pagtipig ang datos

Ang tanan naa sa MySQL: `school_attendance_db.students` ug
`school_attendance_db.attendance`.

## Troubleshooting

| Sayop / Mensahe | Solusyon |
| --- | --- |
| `Can't connect to MySQL server on 'localhost:3306'` | Wala nagdagan ang MySQL. Pindota ang **Start** sa XAMPP. |
| `Unknown database 'school_attendance_db'` | Wala pa na-import ang `schema_attendance.sql`. |
| `Table 'school_attendance_db.students' doesn't exist` | I-import pag-usab ang schema. |
| `Access denied for user 'root'@'localhost'` | I-set ang `DB_PASSWORD`. |
| `ModuleNotFoundError: No module named 'mysql'` | `pip install mysql-connector-python` |
| `Duplicate entry` sa Student ID | Naa na ang estudyante sa masterlist. |

## Backup sa datos

1. Adto sa phpMyAdmin.
2. Pilia ang `school_attendance_db`.
3. **Export** → **Go**.
4. Tipigi ang `.sql` file.

## Sulayi ang code

```powershell
python test.py
```

Dapat `OK` ang mogawas.
