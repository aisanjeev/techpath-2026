# Module 02 — Assignment: Master Your Operating System

**Deadline:** End of Week 2
**Submission:** Document with screenshots + shell script file (.sh)

---

## Task 1: Windows Optimization Report (25 marks)

Optimize your own computer and document what you did:

1. **Startup cleanup** — Open Task Manager → Startup tab
   - List ALL startup apps with their impact level
   - Disable at least 3 unnecessary ones
   - Screenshot the before and after
   - How much faster does your computer boot now? (estimate)

2. **Storage cleanup** — Settings → System → Storage
   - How much total space is used?
   - Run Temporary files cleanup — how much space was reclaimed?
   - List your 3 largest installed apps

3. **Security check**
   - Is Windows Defender active? (screenshot)
   - Is Windows Update current? (screenshot)
   - Are there any Device Manager warnings? (screenshot)

---

## Task 2: Environment Variables Setup (25 marks)

1. Install Python from python.org (if not already installed)
2. Open CMD and type `python --version`
   - If it works → screenshot the output
   - If "not recognized" → find the Python installation path → add to PATH → screenshot the working output
3. Install Git using `winget install Git.Git`
4. Verify: `git --version` (screenshot)
5. Create a custom environment variable called `STUDENT_NAME` with your name
6. Open a NEW CMD window and type `echo %STUDENT_NAME%` (screenshot)

---

## Task 3: Linux First Steps (25 marks)

Install WSL and complete these tasks inside the Linux terminal:

1. Run `wsl --install` in PowerShell (screenshot)
2. After restart, open Ubuntu and create your username
3. Run these commands and screenshot each output:
   - `pwd`
   - `ls -la`
   - `cat /etc/os-release`
   - `free -h`
   - `df -h`
4. Create this folder structure using ONLY terminal commands:
   ```
   ~/my-project/
   ├── src/
   │   ├── main.py
   │   └── utils.py
   ├── tests/
   │   └── test_main.py
   ├── docs/
   │   └── README.md
   └── .gitignore
   ```
5. Write `echo "# My First Project"` into README.md
6. Run `tree ~/my-project/` and screenshot

---

## Task 4: Shell Script (25 marks)

Write a shell script called `system-info.sh` that displays:

- Current date and time
- Your username
- Hostname
- OS information (from `/etc/os-release`)
- CPU info (from `/proc/cpuinfo` — first 5 lines)
- RAM info (from `free -h`)
- Disk usage (from `df -h`)

Make it executable with `chmod +x system-info.sh` and run it. Submit the script file AND a screenshot of its output.

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| Windows Optimization | All tasks done with clear screenshots | Most tasks done | Missing screenshots |
| Environment Variables | PATH working, custom variable set | Python works but no custom var | Python still not recognized |
| Linux Tasks | All commands done, folder structure correct | Most commands, minor errors | WSL not installed |
| Shell Script | Script runs correctly, shows all info | Script runs with minor errors | Script doesn't execute |
