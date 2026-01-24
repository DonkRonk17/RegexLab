# 🔗 RegexLab - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

RegexLab is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: RegexLab + LogHunter](#pattern-1-regexlab--loghunter)
2. [Pattern 2: RegexLab + SynapseLink](#pattern-2-regexlab--synapselink)
3. [Pattern 3: RegexLab + TokenTracker](#pattern-3-regexlab--tokentracker)
4. [Pattern 4: RegexLab + ConfigManager](#pattern-4-regexlab--configmanager)
5. [Pattern 5: RegexLab + DevSnapshot](#pattern-5-regexlab--devsnapshot)
6. [Pattern 6: RegexLab + AgentHandoff](#pattern-6-regexlab--agenthandoff)
7. [Pattern 7: RegexLab + PathBridge](#pattern-7-regexlab--pathbridge)
8. [Pattern 8: RegexLab + GitFlow](#pattern-8-regexlab--gitflow)
9. [Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: RegexLab + LogHunter

**Use Case:** Develop log parsing patterns, then use with LogHunter.

**Why:** Test patterns before running expensive log searches.

**Code:**

```python
from regexlab import RegexLab
from pathlib import Path
# from loghunter import LogHunter  # When available

lab = RegexLab()

# Step 1: Develop pattern with sample log line
sample_log = "2026-01-24 14:30:45 ERROR [BCH] Connection timeout after 30s"

# Test pattern iteratively
lab.test_pattern(r"ERROR \[(\w+)\]", sample_log, show_groups=True)
# Output: Groups: ('BCH',)

# Refine to capture error message too
lab.test_pattern(r"ERROR \[(\w+)\] (.+)", sample_log, show_groups=True)
# Output: Groups: ('BCH', 'Connection timeout after 30s')

# Step 2: Save pattern for production use
lab.add_favorite("bch_error", r"ERROR \[(\w+)\] (.+)", "BCH error with context")

# Step 3: Use verified pattern with LogHunter
# hunter = LogHunter()
# results = hunter.search(r"ERROR \[(\w+)\] (.+)", "/var/log/bch/")
# for result in results:
#     print(f"Component: {result.groups[0]}, Error: {result.groups[1]}")
```

**Result:** Patterns are tested before expensive operations.

---

## Pattern 2: RegexLab + SynapseLink

**Use Case:** Parse @mentions from Synapse messages.

**Why:** Validate mention patterns before deploying to production.

**Code:**

```python
from regexlab import RegexLab
from synapselink import quick_send, SynapseLink

lab = RegexLab()

# Step 1: Develop mention extraction pattern
test_message = "Hey @FORGE and @ATLAS, please review @CLIO's work"

# Test pattern
lab.test_pattern(r"@(\w+)", test_message, show_groups=True)
# Output: 3 matches - FORGE, ATLAS, CLIO

# Step 2: Find all mentions
mentions = lab.find_all(r"@(\w+)", test_message)
print(f"Mentions found: {mentions}")
# Output: ['FORGE', 'ATLAS', 'CLIO']

# Step 3: Use in Synapse message processing
def process_message_with_mentions(message: str) -> dict:
    """Process Synapse message and extract mentions."""
    mentions = lab.find_all(r"@(\w+)", message)
    return {
        "original": message,
        "mentions": mentions,
        "mention_count": len(mentions)
    }

# Step 4: Notify mentioned agents
result = process_message_with_mentions(test_message)
for agent in result["mentions"]:
    quick_send(
        agent,
        "You were mentioned",
        f"In message: {result['original'][:100]}...",
        priority="NORMAL"
    )
```

**Result:** Reliable mention extraction for Synapse coordination.

---

## Pattern 3: RegexLab + TokenTracker

**Use Case:** Optimize regex descriptions for token efficiency.

**Why:** Use library patterns instead of verbose explanations.

**Code:**

```python
from regexlab import RegexLab
# from tokentracker import TokenTracker

lab = RegexLab()
# tracker = TokenTracker()

# INEFFICIENT: Long explanation (many tokens)
# "I need a regex that matches email addresses in the format username@domain.com
#  where username can contain letters, numbers, dots, underscores, etc."
# Token cost: ~50 tokens

# EFFICIENT: Use library reference (few tokens)
email_pattern = lab.get_library_pattern("email")
# Token cost: ~5 tokens for the pattern itself

# Document patterns concisely
pattern_docs = {
    "email": lab.get_library_pattern("email"),
    "phone": lab.get_library_pattern("phone_us"),
    "ip": lab.get_library_pattern("ip_address"),
}

# Track token savings
# original_tokens = tracker.count("Long verbose regex explanation...")
# optimized_tokens = tracker.count(pattern_docs["email"])
# savings = original_tokens - optimized_tokens
```

**Result:** Reduced token usage for pattern-related operations.

---

## Pattern 4: RegexLab + ConfigManager

**Use Case:** Validate regex patterns stored in config files.

**Why:** Catch invalid patterns before runtime errors.

**Code:**

```python
from regexlab import RegexLab
from configmanager import ConfigManager
import re

lab = RegexLab()
config = ConfigManager()

# Step 1: Load config with patterns
cfg = config.load("app_config.json")
# Example config:
# {
#   "validation": {
#     "email_pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
#     "phone_pattern": "\\d{3}-\\d{3}-\\d{4}",
#     "id_pattern": "[A-Z]{2,4}-\\d{4}"
#   }
# }

# Step 2: Validate all patterns on startup
def validate_config_patterns(config_data: dict) -> dict:
    """Validate all regex patterns in config."""
    results = {"valid": [], "invalid": []}
    
    for name, pattern in config_data.get("validation", {}).items():
        try:
            re.compile(pattern)
            lab.test_pattern(pattern, "test_string")
            results["valid"].append(name)
        except re.error as e:
            results["invalid"].append((name, str(e)))
    
    return results

# Step 3: Check patterns
validation = validate_config_patterns(cfg)
if validation["invalid"]:
    print(f"[X] Invalid patterns: {validation['invalid']}")
else:
    print(f"[OK] All {len(validation['valid'])} patterns valid")
```

**Result:** Config validation prevents runtime regex errors.

---

## Pattern 5: RegexLab + DevSnapshot

**Use Case:** Include regex work in development snapshots.

**Why:** Provide context about patterns being developed.

**Code:**

```python
from regexlab import RegexLab
from devsnapshot import DevSnapshot

lab = RegexLab()
snapshot = DevSnapshot()

# Step 1: Work on regex patterns
lab.test_pattern(r"\d{4}-\d{2}-\d{2}", "2026-01-24")
lab.add_favorite("date_parser", r"\d{4}-\d{2}-\d{2}", "ISO date")

# Step 2: Include regex context in snapshot
regex_context = {
    "recent_history": lab._load_history()[-5:],
    "favorites": lab._load_favorites(),
    "patterns_tested": len(lab._load_history())
}

# Step 3: Create snapshot with regex context
snapshot.capture(
    project_path=".",
    additional_context={
        "regexlab": regex_context
    }
)

# Snapshot now includes regex work for debugging/handoff
```

**Result:** Dev snapshots include regex development context.

---

## Pattern 6: RegexLab + AgentHandoff

**Use Case:** Hand off regex work to another agent.

**Why:** Preserve pattern development context across sessions.

**Code:**

```python
from regexlab import RegexLab
from agenthandoff import AgentHandoff

lab = RegexLab()
handoff = AgentHandoff()

# Step 1: Develop patterns (Atlas working on log parser)
lab.test_pattern(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", "2026-01-24 14:30:45")
lab.add_favorite("log_timestamp", r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")

lab.test_pattern(r"(ERROR|WARN|INFO|DEBUG)", "ERROR occurred")
lab.add_favorite("log_level", r"(ERROR|WARN|INFO|DEBUG)")

# Step 2: Create handoff with pattern context
handoff.create(
    from_agent="ATLAS",
    to_agent="FORGE",
    task="Log parser pattern development",
    context={
        "patterns_developed": lab._load_favorites(),
        "test_history": lab._load_history()[-10:],
        "status": "Timestamp and level patterns done, need message extraction",
        "next_pattern": "Extract log message after level"
    }
)

# Step 3: Forge picks up handoff
# handoff_data = handoff.pickup("FORGE")
# patterns = handoff_data["context"]["patterns_developed"]
# for name, info in patterns.items():
#     print(f"Pattern: {name} = {info['pattern']}")
```

**Result:** Seamless regex work handoff between agents.

---

## Pattern 7: RegexLab + PathBridge

**Use Case:** Validate cross-platform file paths.

**Why:** Test path patterns for both Windows and Unix.

**Code:**

```python
from regexlab import RegexLab
from pathbridge import PathBridge

lab = RegexLab()
bridge = PathBridge()

# Step 1: Define platform-specific patterns
WINDOWS_PATH = r"[A-Z]:\\(?:[\w\s.-]+\\)*[\w\s.-]+"
UNIX_PATH = r"/(?:[\w.-]+/)*[\w.-]+"

# Step 2: Test patterns
win_test = "C:\\Users\\logan\\Documents\\file.txt"
unix_test = "/home/logan/documents/file.txt"

lab.test_pattern(WINDOWS_PATH, win_test)
lab.test_pattern(UNIX_PATH, unix_test)

# Step 3: Validate path conversion
def validate_path_conversion(win_path: str, unix_path: str) -> bool:
    """Validate that path conversion preserves validity."""
    # Convert Windows to Unix
    converted = bridge.translate(win_path, "linux")
    
    # Validate converted path matches Unix pattern
    matches = lab.find_all(UNIX_PATH, converted)
    return len(matches) > 0

# Step 4: Use in production
if validate_path_conversion(win_test, unix_test):
    print("[OK] Path conversion valid")
else:
    print("[X] Path conversion failed validation")
```

**Result:** Cross-platform path validation.

---

## Pattern 8: RegexLab + GitFlow

**Use Case:** Validate git commit message formats.

**Why:** Ensure commits follow conventional format.

**Code:**

```python
from regexlab import RegexLab
from gitflow import GitFlow

lab = RegexLab()
git = GitFlow()

# Step 1: Define conventional commit pattern
COMMIT_PATTERN = r"^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"

# Step 2: Test pattern
good_commits = [
    "feat: add new feature",
    "fix(auth): resolve login bug",
    "docs: update README",
]

bad_commits = [
    "Added stuff",
    "WIP",
    "fix typo",
]

# Step 3: Validate commits
print("Good commits:")
for commit in good_commits:
    matches = lab.find_all(COMMIT_PATTERN, commit)
    status = "[OK]" if matches else "[X]"
    print(f"  {status} {commit}")

print("\nBad commits:")
for commit in bad_commits:
    matches = lab.find_all(COMMIT_PATTERN, commit)
    status = "[OK]" if matches else "[X]"
    print(f"  {status} {commit}")

# Step 4: Integrate with GitFlow pre-commit hook
# def validate_commit_message(message: str) -> bool:
#     return bool(lab.find_all(COMMIT_PATTERN, message))
```

**Result:** Commit message validation for consistent git history.

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete log analysis workflow using multiple tools.

**Why:** Demonstrate real production scenario.

**Code:**

```python
from regexlab import RegexLab
from pathlib import Path

lab = RegexLab()

# Step 1: Define patterns
TIMESTAMP_PATTERN = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
LEVEL_PATTERN = r"\b(ERROR|WARN|INFO|DEBUG)\b"
ERROR_MESSAGE_PATTERN = r"ERROR: (.+)"

# Step 2: Test patterns with sample
sample_log = """
2026-01-24 14:30:45 INFO Application started
2026-01-24 14:30:46 DEBUG Loading config
2026-01-24 14:31:00 ERROR: Connection timeout
2026-01-24 14:31:05 WARN Low memory
2026-01-24 14:31:10 ERROR: Database unavailable
"""

# Step 3: Extract data
timestamps = lab.find_all(TIMESTAMP_PATTERN, sample_log)
print(f"Timestamps: {len(timestamps)} found")

levels = lab.find_all(LEVEL_PATTERN, sample_log)
print(f"Log levels: {levels}")

errors = lab.find_all(ERROR_MESSAGE_PATTERN, sample_log)
print(f"Errors: {errors}")

# Step 4: Export for analysis
output_dir = Path.home() / ".regexlab" / "exports"
output_dir.mkdir(exist_ok=True)

lab.export_matches(ERROR_MESSAGE_PATTERN, sample_log, 
                   str(output_dir / "errors.json"), "json")

# Step 5: Save patterns for reuse
lab.add_favorite("log_timestamp", TIMESTAMP_PATTERN, "Log timestamp")
lab.add_favorite("log_level", LEVEL_PATTERN, "Log level")
lab.add_favorite("error_message", ERROR_MESSAGE_PATTERN, "Error extraction")
```

**Result:** Fully instrumented log analysis workflow.

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - RegexLab with full tool ecosystem.

**Why:** Production-grade agent operation.

**Code:**

```python
from regexlab import RegexLab
from synapselink import quick_send
from pathlib import Path

lab = RegexLab()

def full_stack_pattern_development(
    pattern: str,
    test_cases: list,
    pattern_name: str,
    notify_team: bool = True
) -> dict:
    """
    Full-stack pattern development workflow.
    
    1. Test pattern against all cases
    2. Save to favorites if all pass
    3. Export results
    4. Notify team
    """
    results = {
        "pattern": pattern,
        "name": pattern_name,
        "passed": [],
        "failed": [],
        "status": "UNKNOWN"
    }
    
    # Step 1: Test all cases
    for test_case in test_cases:
        text, should_match = test_case
        matches = lab.find_all(pattern, text)
        
        if (len(matches) > 0) == should_match:
            results["passed"].append(text)
        else:
            results["failed"].append(text)
    
    # Step 2: Determine status
    if not results["failed"]:
        results["status"] = "PASS"
        # Save to favorites
        lab.add_favorite(pattern_name, pattern, f"Tested with {len(test_cases)} cases")
    else:
        results["status"] = "FAIL"
    
    # Step 3: Export results
    export_path = Path.home() / ".regexlab" / "test_results" / f"{pattern_name}.json"
    export_path.parent.mkdir(parents=True, exist_ok=True)
    
    import json
    export_path.write_text(json.dumps(results, indent=2))
    
    # Step 4: Notify team
    if notify_team:
        status_icon = "[OK]" if results["status"] == "PASS" else "[X]"
        quick_send(
            "TEAM",
            f"Pattern Development: {pattern_name}",
            f"{status_icon} Status: {results['status']}\n"
            f"Passed: {len(results['passed'])}/{len(test_cases)}\n"
            f"Pattern: {pattern}",
            priority="NORMAL"
        )
    
    return results

# Example usage
test_cases = [
    ("user@example.com", True),
    ("invalid-email", False),
    ("another@test.org", True),
    ("no-at-sign.com", False),
]

result = full_stack_pattern_development(
    pattern=r"^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$",
    test_cases=test_cases,
    pattern_name="email_validator",
    notify_team=True
)

print(f"Result: {result['status']}")
```

**Result:** Production-grade pattern development with full team integration.

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✓ LogHunter - Log analysis patterns
2. ✓ SynapseLink - Message parsing
3. ✓ ConfigManager - Pattern validation

**Week 2 (Productivity):**
4. ☐ DevSnapshot - Context preservation
5. ☐ AgentHandoff - Work handoff
6. ☐ GitFlow - Commit validation

**Week 3 (Advanced):**
7. ☐ PathBridge - Cross-platform paths
8. ☐ TokenTracker - Pattern optimization
9. ☐ Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**
```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from regexlab import RegexLab
```

**Pattern Compilation Errors:**
```python
# Always test patterns before integration
import re
try:
    re.compile(pattern)
except re.error as e:
    print(f"Invalid pattern: {e}")
```

**Windows Console Encoding:**
```python
# For Unicode output on Windows
import sys
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
```

---

**Last Updated:** January 24, 2026  
**Maintained By:** Atlas (Team Brain)
