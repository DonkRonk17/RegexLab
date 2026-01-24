# 🔗 RegexLab - Integration Plan

## 🎯 INTEGRATION GOALS

This document outlines how RegexLab integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - if applicable
4. Logan's workflows

---

## 📦 BCH INTEGRATION

### Overview

RegexLab is primarily a CLI/Python library tool focused on regex testing and pattern validation. BCH integration is **indirect** - agents use RegexLab to develop and test patterns that are then used in BCH message parsing, log analysis, and data validation.

### BCH Use Cases

1. **Message Pattern Validation**: Test patterns for parsing BCH messages
2. **Log Analysis**: Develop patterns for BCH server logs
3. **Input Validation**: Create patterns for user input validation in BCH apps
4. **Data Extraction**: Build patterns for extracting data from BCH conversations

### Example BCH Integration

```python
# In BCH backend, use RegexLab-tested patterns

# Pattern developed and tested with RegexLab:
# python regexlab.py test "@(\w+)" "@CLIO @FORGE please review"
MENTION_PATTERN = r"@(\w+)"

# Use in BCH message processing
import re
def extract_mentions(message: str) -> list:
    """Extract @mentions from BCH message."""
    return re.findall(MENTION_PATTERN, message)
```

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Pattern validation for specs | CLI + Python API | HIGH |
| **Atlas** | Tool development (pattern testing) | CLI + Python API | HIGH |
| **Clio** | Log parsing, data extraction | CLI | HIGH |
| **Nexus** | Cross-platform pattern testing | CLI + Python API | MEDIUM |
| **Bolt** | Quick pattern validation | CLI | MEDIUM |

### Agent-Specific Workflows

#### Forge (Orchestrator / Reviewer)

**Primary Use Case:** Validate patterns in specifications and review pattern-based code.

**Integration Steps:**
1. When reviewing code with regex patterns, test them with RegexLab
2. Validate patterns match expected inputs
3. Document patterns in specifications with RegexLab-verified examples

**Example Workflow:**
```bash
# Forge reviewing a spec with email validation
python regexlab.py library test email "user@example.com"
python regexlab.py library test email "invalid-email"

# Testing custom pattern from spec
python regexlab.py test "^[A-Z]{2,3}-\d{4}$" "BCH-1234"
```

#### Atlas (Executor / Builder)

**Primary Use Case:** Develop and test patterns during tool creation.

**Integration Steps:**
1. Use RegexLab to prototype patterns before implementing
2. Test edge cases with RegexLab before coding
3. Save useful patterns to favorites for reuse

**Example Workflow:**
```python
# Atlas building a log parser
from regexlab import RegexLab

lab = RegexLab()

# Test log parsing pattern
log_line = "2026-01-24 14:30:45 ERROR [main] Connection failed"
lab.test_pattern(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) \[(\w+)\] (.+)",
    log_line,
    show_groups=True
)

# Once verified, use pattern in production code
LOG_PATTERN = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) \[(\w+)\] (.+)"
```

#### Clio (Linux / Ubuntu Agent)

**Primary Use Case:** Parse logs, extract data from system output.

**Platform Considerations:**
- Works natively on Linux without modification
- Combine with grep/awk for powerful text processing
- Use in shell scripts for data extraction

**Example:**
```bash
# Clio analyzing system logs
python3 regexlab.py find "ERROR|WARN" "$(cat /var/log/syslog | head -100)"

# Extract IP addresses from network output
python3 regexlab.py find "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" "$(netstat -an)"

# Save useful patterns
python3 regexlab.py favorite add syslog_error "(\w+ \d+ \d+:\d+:\d+) \w+ (\w+): (.+)"
```

#### Nexus (Multi-Platform Agent)

**Primary Use Case:** Cross-platform pattern testing and validation.

**Cross-Platform Notes:**
- Same patterns work on Windows, Linux, macOS
- Config files stored in user home directory (`~/.regexlab/`)
- No platform-specific dependencies

**Example:**
```python
from regexlab import RegexLab
import platform

lab = RegexLab()

# Platform-aware path pattern
if platform.system() == "Windows":
    path_pattern = r"[A-Z]:\\(?:[\w\s.-]+\\)*[\w\s.-]+"
else:
    path_pattern = r"/(?:[\w.-]+/)*[\w.-]+"

lab.test_pattern(path_pattern, some_path)
```

#### Bolt (Cline / Free Executor)

**Primary Use Case:** Quick pattern validation without API costs.

**Cost Considerations:**
- RegexLab is 100% local - no API calls
- Reduces need for AI-assisted regex help
- Pattern library provides instant answers

**Example:**
```bash
# Bolt validating input patterns (no API needed!)
python regexlab.py library list
python regexlab.py library test email "user@domain.com"
python regexlab.py library test phone_us "(555) 123-4567"
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With LogHunter

**Log Analysis Use Case:** Develop patterns for LogHunter searches.

**Integration Pattern:**
```python
from regexlab import RegexLab
# from loghunter import LogHunter  # When available

lab = RegexLab()

# Step 1: Develop pattern with RegexLab
sample_log = "2026-01-24 14:30:45 ERROR [BCH] Connection timeout"
lab.test_pattern(r"ERROR \[(\w+)\] (.+)", sample_log, show_groups=True)

# Step 2: Once verified, use in LogHunter
# hunter = LogHunter()
# results = hunter.search(r"ERROR \[(\w+)\] (.+)", "/var/log/bch/")
```

### With SynapseLink

**Message Parsing Use Case:** Validate patterns for Synapse message parsing.

**Integration Pattern:**
```python
from regexlab import RegexLab
from synapselink import SynapseLink

lab = RegexLab()
synapse = SynapseLink()

# Test mention extraction pattern
msg = "Hey @FORGE and @ATLAS, please review this"
lab.test_pattern(r"@(\w+)", msg, show_groups=True)

# Verified pattern - use in production
MENTION_PATTERN = r"@(\w+)"
mentions = lab.find_all(MENTION_PATTERN, synapse.get_latest_message())
```

### With TokenTracker

**Token Optimization Use Case:** Compress regex patterns to save tokens.

**Integration Pattern:**
```python
from regexlab import RegexLab
# from tokentracker import TokenTracker

lab = RegexLab()
# tracker = TokenTracker()

# Document patterns concisely for token savings
# Instead of explaining: "Match emails with standard format..."
# Use: lab.get_library_pattern("email")
email_pattern = lab.get_library_pattern("email")
# Result: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

### With ConfigManager

**Configuration Use Case:** Validate config file patterns.

**Integration Pattern:**
```python
from regexlab import RegexLab
from configmanager import ConfigManager

lab = RegexLab()
config = ConfigManager()

# Load config with patterns
cfg = config.load("app_config.json")

# Validate patterns are correct
for name, pattern in cfg.get("validation_patterns", {}).items():
    print(f"Testing pattern: {name}")
    lab.test_pattern(pattern, cfg.get(f"{name}_example", "test"))
```

### With DevSnapshot

**Debugging Use Case:** Include RegexLab history in dev snapshots.

**Integration Pattern:**
```python
from regexlab import RegexLab
from devsnapshot import DevSnapshot

lab = RegexLab()
snapshot = DevSnapshot()

# Include pattern history in debug context
history = lab._load_history()
snapshot.add_context("regexlab_history", history[-5:])  # Last 5 patterns

# Take snapshot with regex context
snapshot.capture()
```

### With AgentHandoff

**Handoff Use Case:** Include regex work in handoff context.

**Integration Pattern:**
```python
from regexlab import RegexLab
from agenthandoff import AgentHandoff

lab = RegexLab()
handoff = AgentHandoff()

# Working on log parser - save context for handoff
lab.add_favorite("log_parser_wip", r"(\d{4}-\d{2}-\d{2}) (\w+) (.+)")

# Create handoff with pattern context
handoff.create(
    from_agent="ATLAS",
    to_agent="FORGE",
    context={
        "task": "Log parser development",
        "patterns_developed": lab._load_favorites(),
        "test_results": "See EXAMPLES.md"
    }
)
```

### With PathBridge

**Path Pattern Use Case:** Test cross-platform path patterns.

**Integration Pattern:**
```python
from regexlab import RegexLab
from pathbridge import PathBridge

lab = RegexLab()
bridge = PathBridge()

# Test Windows path pattern
win_pattern = r"[A-Z]:\\(?:[\w\s.-]+\\)*[\w\s.-]+"
lab.test_pattern(win_pattern, "C:\\Users\\logan\\Documents\\file.txt")

# Test Unix path pattern
unix_pattern = r"/(?:[\w.-]+/)*[\w.-]+"
lab.test_pattern(unix_pattern, "/home/logan/documents/file.txt")

# Use PathBridge for conversion, RegexLab for validation
converted_path = bridge.translate(windows_path, "linux")
assert lab.find_all(unix_pattern, converted_path)
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)

**Goal:** All agents aware and can use basic features

**Steps:**
1. ✓ Tool deployed to GitHub
2. ☐ Quick-start guides sent via Synapse
3. ☐ Each agent tests basic workflow
4. ☐ Feedback collected

**Success Criteria:**
- All 5 agents have used tool at least once
- No blocking issues reported

### Phase 2: Integration (Week 2-3)

**Goal:** Integrated into daily workflows

**Steps:**
1. ☐ Add to agent startup patterns (test common patterns)
2. ☐ Create integration examples with existing tools
3. ☐ Build shared pattern library
4. ☐ Monitor usage patterns

**Success Criteria:**
- Used daily by at least 3 agents
- Integration examples tested

### Phase 3: Optimization (Week 4+)

**Goal:** Optimized and fully adopted

**Steps:**
1. ☐ Collect efficiency metrics
2. ☐ Implement v1.1 improvements
3. ☐ Create advanced workflow examples
4. ☐ Full Team Brain ecosystem integration

**Success Criteria:**
- Measurable time savings
- Positive feedback from all agents
- v1.1 improvements identified

---

## 📊 SUCCESS METRICS

**Adoption Metrics:**
- Number of agents using tool: [Track]
- Daily usage count: [Track]
- Patterns saved to favorites: [Track]
- Library patterns used: [Track]

**Efficiency Metrics:**
- Time saved per regex task: ~5-10 minutes
- Reduced debugging time: ~50%
- Pattern reuse rate: [Track]

**Quality Metrics:**
- Bug reports: [Track]
- Feature requests: [Track]
- User satisfaction: [Qualitative]

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths

```python
# Standard import
from regexlab import RegexLab

# Specific class access
lab = RegexLab()

# Library pattern access
pattern = lab.get_library_pattern("email")
```

### Configuration Integration

**Config File:** `~/.regexlab/`
- `history.json` - Pattern history (last 50)
- `favorites.json` - Saved patterns

**Shared Config with Other Tools:**
```python
# RegexLab respects user home directory
from pathlib import Path
config_dir = Path.home() / ".regexlab"
```

### Error Handling Integration

**Standardized Exit Codes:**
- 0: Success
- 1: General error / Pattern error

**Error Messages:**
- `[X] Invalid regex pattern: <error>` - Malformed regex
- `[X] Pattern not found in library` - Unknown library pattern
- `[X] Export failed: <error>` - File write error

### Logging Integration

RegexLab logs to history file, not system logs. For system logging integration:

```python
import logging
from regexlab import RegexLab

# Configure logging if needed
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("regexlab")

lab = RegexLab()
# RegexLab operations...
```

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy

- Minor updates (v1.x): As needed
- Major updates (v2.0+): Quarterly review
- Security patches: Immediate

### Support Channels

- GitHub Issues: Bug reports
- Synapse: Team Brain discussions
- Direct to Builder: Complex issues

### Known Limitations

- Unicode output may fail on Windows console (use ASCII)
- History limited to 50 entries
- No interactive mode (CLI only)

### Planned Improvements

- [ ] Interactive REPL mode
- [ ] Pattern testing with file input
- [ ] Pattern visualization
- [ ] Web UI (future)

---

## 📚 ADDITIONAL RESOURCES

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Start Guides: [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)
- GitHub: https://github.com/DonkRonk17/RegexLab

---

**Last Updated:** January 24, 2026  
**Maintained By:** Atlas (Team Brain)
