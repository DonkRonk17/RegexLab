<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/6c4d852d-e2a2-4324-945a-8193d2ef94a4" />

# 🧪 RegexLab - Interactive Regex Tester and Pattern Library

**Version:** 1.0.0  
**Author:** Logan Smith / Metaphy LLC  
**License:** MIT  
**GitHub:** https://github.com/DonkRonk17/RegexLab

---

## 📖 Overview

**RegexLab** is a powerful command-line regex testing and pattern management tool. Test patterns instantly, access a comprehensive pattern library, and manage your favorite regex expressions - all with **zero external dependencies**.

Perfect for developers who need to quickly test and debug regex patterns without opening a browser or installing heavyweight tools.

---

## ✨ Features

### 🧪 Interactive Testing
- **Live Pattern Testing** - Test regex against any text instantly
- **Match Highlighting** - See exactly what matched with `>>>match<<<` markers
- **Group Extraction** - View capturing groups and named groups
- **Multiple Flags** - Support for case-insensitive, multiline, dotall modes

### 📚 Pattern Library
- **12 Built-in Patterns** - Email, URL, phone, IP, dates, and more
- **One-Command Testing** - Test library patterns instantly
- **Documented Examples** - Each pattern includes description and example

### 💾 Pattern Management
- **History Tracking** - Automatically saves last 50 patterns tested
- **Favorites System** - Save frequently used patterns with custom names
- **Quick Access** - Retrieve and reuse patterns anytime

### 🔧 Advanced Operations
- **Find All Matches** - Extract all matches from text
- **Replace Preview** - See replacement results before applying
- **Text Splitting** - Split text using regex patterns
- **Export Matches** - Save matches to JSON, CSV, or TXT

### 🎯 Core Advantages
- **Zero Dependencies** - Pure Python standard library
- **Cross-Platform** - Works on Windows, Linux, macOS
- **Fast & Lightweight** - Instant startup and execution
- **CLI Native** - Perfect for scripts and automation

---

## 🚀 Installation

### Option 1: Direct Installation (Recommended)
```bash
# Clone or download
git clone https://github.com/DonkRonk17/RegexLab.git
cd RegexLab

# Install
pip install .

# Or install in development mode
pip install -e .
```

### Option 2: Manual Setup
```bash
# Make executable (Linux/macOS)
chmod +x regexlab.py

# Run directly
python3 regexlab.py --help

# Or add to PATH
sudo ln -s $(pwd)/regexlab.py /usr/local/bin/regexlab
```

### Option 3: Windows Portable
```powershell
# Add to PATH or run directly
python regexlab.py --help
```

---

## 📚 Usage

### Basic Pattern Testing

**Test a simple pattern:**
```bash
regexlab test "\d+" "abc 123 def 456"
# Matches: 123, 456
```

**Case-insensitive matching:**
```bash
regexlab test "[a-z]+" "ABC def GHI" -i
# Matches: ABC, def, GHI
```

**Show capturing groups:**
```bash
regexlab test "(\w+)@(\w+)\.(\w+)" "user@example.com" -g
# Shows: ('user', 'example', 'com')
```

**Multiline mode:**
```bash
regexlab test "^line" "first line\nsecond line" -m
# Matches at start of each line
```

---

### Pattern Library

**List all built-in patterns:**
```bash
regexlab library list
```

**Test a library pattern:**
```bash
# Email validation
regexlab library test email "user@example.com"

# URL validation
regexlab library test url "https://github.com/user/repo"

# Phone number
regexlab library test phone_us "(555) 123-4567"

# IP address
regexlab library test ip_address "192.168.1.1"

# Date format
regexlab library test date_iso "2026-01-15"
```

**Available Library Patterns:**
- `email` - Email address validation
- `url` - HTTP/HTTPS URL matching
- `phone_us` - US phone number (various formats)
- `ip_address` - IPv4 address
- `date_iso` - ISO date format (YYYY-MM-DD)
- `time_24h` - 24-hour time (HH:MM)
- `hex_color` - Hexadecimal color codes
- `username` - Username validation (3-16 chars)
- `password_strong` - Strong password requirements
- `credit_card` - Credit card number format
- `ssn` - US Social Security Number
- `zip_code_us` - US ZIP codes (5 or 9 digits)

---

### Finding and Extracting

**Find all matches:**
```bash
regexlab find "\d+" "Order #123, Total: $456, ID: 789"
# Returns: ['123', '456', '789']
```

**Extract email addresses from text:**
```bash
regexlab find "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" "Contact: john@example.com or support@test.org"
# Returns: ['john@example.com', 'support@test.org']
```

---

### Replace and Transform

**Preview replacements:**
```bash
regexlab replace "\d+" "X" "Order #123, Total: $456"
# Preview: Order #X, Total: $X
```

**Limit replacement count:**
```bash
regexlab replace "\d+" "NUM" "1 2 3 4 5" -c 2
# Result: NUM NUM 3 4 5
```

**Case-insensitive replace:**
```bash
regexlab replace "error" "SUCCESS" "Error in line 1, ERROR in line 2" -i
# Result: SUCCESS in line 1, SUCCESS in line 2
```

---

### Text Splitting

**Split by delimiter:**
```bash
regexlab split "," "apple,banana,cherry"
# Returns: ['apple', 'banana', 'cherry']
```

**Split by multiple whitespace:**
```bash
regexlab split "\s+" "word1   word2\tword3\nword4"
# Returns: ['word1', 'word2', 'word3', 'word4']
```

---

### Pattern History

**View recent patterns:**
```bash
regexlab history

# Show last 20 patterns
regexlab history -n 20
```

---

### Favorite Patterns

**Save a pattern:**
```bash
regexlab favorite add my_pattern "\d{3}-\d{4}" --description "Phone extension format"
```

**List favorites:**
```bash
regexlab favorite list
```

**Use a favorite** (copy pattern from list and use in test)

---

### Export Matches

**Export to JSON:**
```bash
regexlab export "\d+" "Numbers: 123, 456, 789" matches.json
```

**Export to CSV:**
```bash
regexlab export "[a-z]+" "hello world test" words.csv -f csv
```

**Export to text file:**
```bash
regexlab export "\w+@\w+\.\w+" "Emails: a@b.c and x@y.z" emails.txt -f txt
```

---

## 💡 Use Cases

### Email Validation in Scripts
```bash
#!/bin/bash
email="user@example.com"
regexlab library test email "$email"
# Exit code 0 if valid, use in conditionals
```

### Extract Data from Logs
```bash
# Extract all IP addresses from log file
cat access.log | while read line; do
    regexlab find "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" "$line"
done
```

### Data Cleaning
```bash
# Remove all non-alphanumeric characters
regexlab replace "[^a-zA-Z0-9\s]" "" "Hello, World! #2026"
# Result: Hello World 2026
```

### Quick Pattern Testing
```bash
# Test if string matches password requirements
regexlab library test password_strong "MyP@ssw0rd"
```

---

## 🗂️ Configuration

RegexLab stores data in `~/.regexlab/`:

```
~/.regexlab/
├── history.json     # Last 50 tested patterns
└── favorites.json   # Saved favorite patterns
```

### History Format
```json
[
  {
    "pattern": "\\d+",
    "test_string": "abc 123",
    "flags": 0,
    "timestamp": "2026-01-15T10:30:00"
  }
]
```

### Favorites Format
```json
{
  "my_pattern": {
    "pattern": "\\d{3}-\\d{4}",
    "description": "Phone extension",
    "created": "2026-01-15T10:30:00"
  }
}
```

---

## 🧪 Regex Flags

RegexLab supports standard Python regex flags:

- `-i` / `--ignorecase` - Case-insensitive matching
- `-m` / `--multiline` - `^` and `$` match line boundaries
- `-s` / `--dotall` - `.` matches newlines
- `-g` / `--groups` - Display capturing groups

---

## 📖 Pattern Syntax Quick Reference

**Basic:**
- `.` - Any character (except newline)
- `\d` - Digit (0-9)
- `\w` - Word character (a-z, A-Z, 0-9, _)
- `\s` - Whitespace

**Quantifiers:**
- `*` - 0 or more
- `+` - 1 or more
- `?` - 0 or 1
- `{n}` - Exactly n times
- `{n,m}` - Between n and m times

**Anchors:**
- `^` - Start of string/line
- `$` - End of string/line
- `\b` - Word boundary

**Groups:**
- `(...)` - Capturing group
- `(?:...)` - Non-capturing group
- `(?P<name>...)` - Named group

---
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/777daf84-e810-4fb4-96b3-1216d0b4edc1" />

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new patterns
4. Submit a Pull Request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Credits

Created by **Randell Logan Smith and Team Brain** at [Metaphy LLC](https://metaphysicsandcomputing.com)

Part of the HMSS (Heavenly Morning Star System) ecosystem.

---

## 🔗 Links

- **GitHub:** https://github.com/DonkRonk17/RegexLab
- **Issues:** https://github.com/DonkRonk17/RegexLab/issues
- **Author:** https://github.com/DonkRonk17

---

**RegexLab** - Test, Learn, Master Regex! 🧪
