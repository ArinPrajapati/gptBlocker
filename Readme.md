# GPT Blocker (Windows & Linux)

## 📌 Overview
This is a simple Python script that blocks or unblocks chatgpt and any website by modifying the system's `hosts` file. It works on both **Windows** and **Linux**.

## 🔹 Features
✅ Blocks websites system-wide (all browsers).  
✅ Unblocks websites easily.  
✅ Works on both **Windows** and **Linux**.  
✅ Lightweight and easy to use.  
✅ Requires **Administrator/Root** privileges.

---

## ⚡ Installation
### 1️⃣ **Clone the Repository**
```sh
git clone git@github.com:ArinPrajapati/gptBlocker.git
cd gptBlocker
```

### 2️⃣ **Install Python (if not installed)**
Ensure you have Python installed (version 3.x recommended). You can check with:
```sh
python --version
```

---

## 🚀 Usage
### **Run as Administrator (Windows) or Root (Linux)**
- **Windows:** Right-click `cmd` and select **"Run as Administrator"**.
- **Linux:** Use `sudo` before the command.

### **Block Websites**
```sh
python main.py block
```

```sh
python3 main.py block
```

### **Unblock Websites**
```sh
python main.py unblock
```
```sh
python3 main.py unblock
```
### **Modify Blocked Websites**
Edit the `BLOCKED_SITES` list in `main.py` to add or remove websites.

---

## ⚠️ Notes
- You must **restart your browser** for changes to take effect.
- If sites are still accessible, **clear browser cache** or restart your computer.
- To block network-wide, use **DNS filtering** (e.g., OpenDNS) or **Pi-hole**.

---

## 🔧 Troubleshooting
❌ **Permission Denied:** Run the script as **Administrator (Windows)** or **Root (Linux)**.  
❌ **Changes not working?** Restart your browser or flush DNS:
- **Windows:** `ipconfig /flushdns`
- **Linux:** `sudo systemctl restart networking`

---

## 📜 License
This project is open-source and free to use under the MIT License.

## 🤝 Contributing
Feel free to fork this repo and submit a pull request!

## 📩 Contact
For questions or issues, open an **issue** in the GitHub repository.

---
🚀 Happy Blocking! 🚀

