# 🏀 Basketball Court Reservation Bot

This is a high-precision Selenium bot that logs into AvalonAccess.com and automatically reserves a Basketball Court **at exactly 12:00:00 AM** for the next day.

It navigates the portal, refreshes the reservation page at midnight, fills the form using optimized DOM access, and submits the reservation **within milliseconds** — ensuring you never miss a spot.

---

## 🚀 Features

- Logs in 2 minutes before midnight
- Navigates to the Basketball Court reservation form
- Refreshes at **12:00:00.000 AM** to load the next day’s date
- Dynamically selects the correct time slot using the day of the week
- Instantly fills form using JavaScript (faster than `send_keys`)
- Submits by **12:00:00.200 AM**
- Precision logs for every step
- Checks clock every **1ms**, logs every **10 seconds**

---

## 🧩 Tech Stack

- Python 3.8+
- Selenium
- webdriver-manager
- python-dotenv

---

## 📁 Folder Structure

```
court_bot/
├── court_reservation_bot.py   # ✅ Main script
├── .env                       # 🔒 Sensitive credentials
├── README.md                  # 📘 You're reading it
```

---

## 🔐 .env Configuration

Create a `.env` file in the project folder:

```env
COURT_URL=https://your_url/
USERNAME=your_email@example.com
PASSWORD=your_password
AMENITY_ID=the_HTML_element_ID_value
```

> ⚠️ Never commit `.env` to version control.

---

## 📦 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/aayush912/court_bot.git
cd court_bot
```

### 2. Create and Activate Environment

Using Conda:

```bash
conda create --name court_bot python=3.10 -y
conda activate court_bot
```

Or using venv:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Packages

```bash
pip install selenium webdriver-manager python-dotenv
```

---

## ⚙️ How to Use

Run the script **any time between 11:58 PM and 11:59 PM**:

```bash
python court_reservation_bot.py
```

What it does:

1. Logs in to your URL
2. Opens Basketball Court reservation page
3. Waits until exactly `12:00:00.000`
4. Refreshes page → fills next day's date and details
5. Dynamically builds time slot (e.g. `Monday-7:00 PM-8:00 PM `)
6. Submits instantly via JavaScript injection

---

## 🧪 Sample Output

```
[WAIT] Time now: 23:59:50 — still waiting...
[WAIT] Hit target: 00:00:00.000
[PERF] Page refreshed in 121.87 ms
[FORM] Target slot: Monday-11:00 AM-12:00 PM  for m/d/yyyy
[PERF] Form filled in 233.76 ms
[SUBMIT] Clicking Reserve at 00:00:00.200
[PERF] Submit clicked in 25.14 ms
✅ Reservation submitted successfully!
```

---

## ✅ Optimization Summary

| Optimization                     | Result                    |
|----------------------------------|---------------------------|
| JavaScript `value` injection     | Instant form fill         |
| `select_by_value()` with dynamic day | Instant slot selection     |
| DOM elements cached              | Less browser overhead     |
| No unnecessary delays            | Faster overall            |
| `time.sleep(0.001)` + log every 10s | Accurate + readable       |

---

## 💡 Optional Enhancements

- Schedule with `cron` (macOS/Linux) or Task Scheduler (Windows)
- Add SMS/email notifications
- Retry fallback if the time slot is unavailable
- Capture screenshots on success/failure

---

## 📝 Author

Built by Aayush Kumar Verma