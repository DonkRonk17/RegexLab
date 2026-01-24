# ⚡ RegexLab - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Executor)](#atlas-quick-start)
- [Clio (Linux Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to validate and test regex patterns for specifications and code review

### Step 1: Installation Check

```bash
# Verify RegexLab is available
cd C:\Users\logan\OneDrive\Documents\AutoProjects\RegexLab
python regexlab.py --help

# Expected: Help message with available commands
```

### Step 2: First Use - Pattern Validation

When reviewing a spec or code that includes regex patterns, validate them:

```bash
# Test a pattern from a spec
python regexlab.py test "^[A-Z]{2,4}-\d{4}$" "BCH-1234"

# Expected output:
# [OK] 1 match(es) found
# Match #1: Position: 0-8, Matched: 'BCH-1234'
```

### Step 3: Library Pattern Verification

Check if standard patterns are used correctly:

```bash
# List available library patterns
python regexlab.py library list

# Test email pattern from library
python regexlab.py library test email "user@example.com"
python regexlab.py library test email "invalid-email"  # Should fail
```

### Step 4: Common Forge Commands

```bash
# Validate pattern in spec
python regexlab.py test "PATTERN_FROM_SPEC" "TEST_STRING"

# Check multiple test cases
python regexlab.py test "\d{3}-\d{4}" "555-1234"
python regexlab.py test "\d{3}-\d{4}" "invalid"

# View pattern with groups for data extraction specs
python regexlab.py test "(\w+)@(\w+\.\w+)" "user@domain.com" -g
```

### Next Steps for Forge

1. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
2. Use during spec reviews to validate patterns
3. Request pattern additions to library if common patterns missing

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to develop and test patterns during tool creation

### Step 1: Installation Check

```bash
# Verify import works
python -c "from regexlab import RegexLab; print('[OK] RegexLab ready')"
```

### Step 2: First Use - Pattern Development

Before implementing regex in your tools, test them:

```bash
# Test pattern you're planning to use
python regexlab.py test "\d{4}-\d{2}-\d{2}" "Log entry: 2026-01-24 started"

# See match position and highlighted result
# Use this to verify pattern before coding
```

### Step 3: Python API for Tool Integration

```python
from regexlab import RegexLab

lab = RegexLab()

# Test pattern during development
lab.test_pattern(r"\d{4}-\d{2}-\d{2}", "Today is 2026-01-24")

# Find all matches programmatically
matches = lab.find_all(r"\d+", "abc 123 def 456")
print(matches)  # ['123', '456']

# Test replacement
result = lab.replace_pattern(r"\d+", "X", "abc 123 def 456")
print(result)  # abc X def X

# Save useful patterns for reuse
lab.add_favorite("date_iso", r"\d{4}-\d{2}-\d{2}", "ISO date format")
```

### Step 4: Common Atlas Commands

```bash
# Prototype pattern
python regexlab.py test "PATTERN" "TEST_TEXT"

# Test with groups (for data extraction)
python regexlab.py test "(\w+)=(\d+)" "count=42" -g

# Find all occurrences
python regexlab.py find "\w+Error" "ConnectionError: TimeoutError: ValueError"

# Save for reuse
python regexlab.py favorite add mypattern "\d+-\w+" --description "ID format"
```

### Next Steps for Atlas

1. Use RegexLab before implementing any regex in tools
2. Save commonly used patterns to favorites
3. Integrate into test suites for pattern validation

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to use RegexLab for log parsing and text extraction

### Step 1: Linux Installation

```bash
# Clone from GitHub (if not already available)
cd ~/tools
git clone https://github.com/DonkRonk17/RegexLab.git
cd RegexLab

# Verify
python3 regexlab.py --version
```

### Step 2: First Use - Log Analysis

```bash
# Parse log entry
python3 regexlab.py test "(\w+ \d+ \d+:\d+:\d+) \w+ (\w+): (.+)" \
    "Jan 24 14:30:45 server sshd: Connection from 192.168.1.1"

# Extract all IPs from netstat output
python3 regexlab.py find "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" "$(netstat -an | head -20)"
```

### Step 3: Integration with Shell Pipelines

```bash
# Extract errors from syslog
grep "ERROR" /var/log/syslog | python3 regexlab.py find "ERROR: (.+)" "$(cat -)"

# Export matches to file
python3 regexlab.py export "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" \
    "$(cat /var/log/auth.log | head -100)" ips.txt -f txt
```

### Step 4: Common Clio Commands

```bash
# Test syslog pattern
python3 regexlab.py test "(\w+ \d+ \d+:\d+:\d+) \S+ (\w+)\[(\d+)\]: (.+)" \
    "Jan 24 10:30:00 server sshd[1234]: Accepted password"

# Find all URLs in file
python3 regexlab.py find "https?://[^\s]+" "$(cat webpage.html)"

# List library patterns
python3 regexlab.py library list
```

### Next Steps for Clio

1. Add to ABIOS startup for pattern validation
2. Create shell aliases for common patterns
3. Report Linux-specific issues via Synapse

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform usage of RegexLab

### Step 1: Platform Detection

```python
import platform
from regexlab import RegexLab

lab = RegexLab()
print(f"Platform: {platform.system()}")
print(f"Config dir: {lab.config_dir}")
```

### Step 2: First Use - Cross-Platform Testing

```bash
# Same commands work everywhere
python regexlab.py test "\d+" "test 123"
python regexlab.py library test email "user@test.com"
```

### Step 3: Platform-Specific Patterns

```python
from regexlab import RegexLab
import platform

lab = RegexLab()

# Platform-aware path validation
if platform.system() == "Windows":
    path_pattern = r"[A-Z]:\\(?:[\w\s.-]+\\)*[\w\s.-]+"
    test_path = "C:\\Users\\logan\\file.txt"
else:
    path_pattern = r"/(?:[\w.-]+/)*[\w.-]+"
    test_path = "/home/user/file.txt"

lab.test_pattern(path_pattern, test_path)

# Both platforms use same config structure
lab.add_favorite("path_pattern", path_pattern, f"{platform.system()} paths")
```

### Step 4: Common Nexus Commands

```bash
# Cross-platform commands
python regexlab.py test "\w+@\w+\.\w+" "user@test.com"  # Works everywhere
python regexlab.py library list  # Same library everywhere
python regexlab.py history  # History persists per-platform
```

### Next Steps for Nexus

1. Test on all 3 platforms
2. Document platform-specific patterns
3. Report cross-platform issues

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to use RegexLab without API costs

### Step 1: Verify Free Access

```bash
# No API key needed!
python regexlab.py --help

# All features work locally
python regexlab.py library list
```

### Step 2: First Use - Quick Validation

Instead of asking AI to write regex, use the library:

```bash
# Need email validation? It's built-in!
python regexlab.py library test email "test@example.com"

# Need phone validation?
python regexlab.py library test phone_us "555-123-4567"

# Need IP validation?
python regexlab.py library test ip_address "192.168.1.1"
```

### Step 3: Cost-Free Pattern Development

```bash
# Develop patterns locally (no API calls!)
python regexlab.py test "\d{3}-\d{4}" "555-1234"

# Iterate until correct
python regexlab.py test "\d{3}-\d{3}-\d{4}" "555-123-4567"

# Save for reuse
python regexlab.py favorite add phone_local "\d{3}-\d{4}" "Local phone"
```

### Step 4: Common Bolt Commands

```bash
# Quick pattern check
python regexlab.py test "PATTERN" "TEXT"

# Use library patterns
python regexlab.py library test email "email@test.com"

# Check history (no AI needed to remember!)
python regexlab.py history

# Export results for other tools
python regexlab.py export "\d+" "1 2 3 4 5" numbers.json
```

### Next Steps for Bolt

1. Use RegexLab instead of AI for regex questions
2. Build up favorites for common tasks
3. Report issues via Synapse

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/RegexLab/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message Atlas for complex issues

---

## 🎯 QUICK REFERENCE: ALL COMMANDS

```bash
# Testing
python regexlab.py test PATTERN TEXT [-i] [-m] [-s] [-g]

# Library
python regexlab.py library list
python regexlab.py library test NAME TEXT

# Find/Replace/Split
python regexlab.py find PATTERN TEXT [-i]
python regexlab.py replace PATTERN REPLACEMENT TEXT [-i] [-c N]
python regexlab.py split PATTERN TEXT [-i]

# Favorites & History
python regexlab.py favorite add NAME PATTERN [--description DESC]
python regexlab.py favorite list
python regexlab.py history [-n COUNT]

# Export
python regexlab.py export PATTERN TEXT OUTPUT [-f json|csv|txt]
```

---

**Last Updated:** January 24, 2026  
**Maintained By:** Atlas (Team Brain)
