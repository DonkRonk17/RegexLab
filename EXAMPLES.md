# 📚 RegexLab - Usage Examples

Complete examples demonstrating all RegexLab features with expected output.

**Quick Navigation:**
- [Example 1: Basic Pattern Testing](#example-1-basic-pattern-testing)
- [Example 2: Using Pattern Library](#example-2-using-pattern-library)
- [Example 3: Finding All Matches](#example-3-finding-all-matches)
- [Example 4: Pattern Replacement](#example-4-pattern-replacement)
- [Example 5: Text Splitting](#example-5-text-splitting)
- [Example 6: Using Flags (Case-Insensitive)](#example-6-using-flags-case-insensitive)
- [Example 7: Managing Favorites](#example-7-managing-favorites)
- [Example 8: Viewing History](#example-8-viewing-history)
- [Example 9: Exporting Matches](#example-9-exporting-matches)
- [Example 10: Capturing Groups](#example-10-capturing-groups)
- [Example 11: Email Validation Workflow](#example-11-email-validation-workflow)
- [Example 12: Log File Analysis](#example-12-log-file-analysis)

---

## Example 1: Basic Pattern Testing

**Scenario:** Test if a pattern matches a string and see where matches occur.

**Command:**
```bash
python regexlab.py test "\d+" "abc 123 def 456 ghi 789"
```

**Expected Output:**
```
[OK] Pattern: \d+
[OK] Flags: None
[OK] Test String: abc 123 def 456 ghi 789
----------------------------------------------------------------------
[OK] 3 match(es) found

Match #1:
  Position: 4-7
  Matched: '123'

Match #2:
  Position: 12-15
  Matched: '456'

Match #3:
  Position: 20-23
  Matched: '789'

Highlighted text:
  abc >>>123<<< def >>>456<<< ghi >>>789<<<
```

**What You Learned:**
- How to test a basic regex pattern
- Match positions are shown as start-end indices
- Matched text is highlighted with `>>><<<` markers

---

## Example 2: Using Pattern Library

**Scenario:** Use pre-built patterns from the library for common validation tasks.

**List All Library Patterns:**
```bash
python regexlab.py library list
```

**Expected Output (partial):**
```
[OK] RegexLab Pattern Library:
----------------------------------------------------------------------

email:
  Pattern: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
  Description: Standard email address format
  Example: user@example.com

phone_us:
  Pattern: ^\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$
  Description: US phone number (various formats)
  Example: (555) 123-4567

ip_address:
  Pattern: ^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}...
  Description: IPv4 address
  Example: 192.168.1.1
```

**Test Library Pattern:**
```bash
python regexlab.py library test email "user@example.com"
```

**Expected Output:**
```
[OK] Testing library pattern: email
[OK] Pattern: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
[OK] Flags: None
[OK] Test String: user@example.com
----------------------------------------------------------------------
[OK] 1 match(es) found

Match #1:
  Position: 0-16
  Matched: 'user@example.com'
```

**What You Learned:**
- Access 12+ pre-built patterns for common validation
- Test library patterns directly against your input
- Save time by not writing common patterns from scratch

---

## Example 3: Finding All Matches

**Scenario:** Extract all occurrences of a pattern from text.

**Command:**
```bash
python regexlab.py find "[A-Z][a-z]+" "Hello World, this is RegexLab"
```

**Expected Output:**
```
[OK] Found 4 match(es)
  1. Hello
  2. World
  3. RegexLab
```

**What You Learned:**
- Find command returns all matches as a list
- Great for extracting data from larger text
- Results are numbered for easy reference

---

## Example 4: Pattern Replacement

**Scenario:** Replace all phone numbers with a masked version.

**Basic Replacement:**
```bash
python regexlab.py replace "\d{3}-\d{4}" "XXX-XXXX" "Call me at 555-1234 or 555-5678"
```

**Expected Output:**
```
[OK] Would replace 2 occurrence(s)

Original:
  Call me at 555-1234 or 555-5678

Result:
  Call me at XXX-XXXX or XXX-XXXX
```

**Limited Replacement (first match only):**
```bash
python regexlab.py replace "\d+" "NUM" "1 2 3 4 5" -c 2
```

**Expected Output:**
```
[OK] Would replace 2 occurrence(s)

Original:
  1 2 3 4 5

Result:
  NUM NUM 3 4 5
```

**What You Learned:**
- Preview replacements before applying them
- Use `-c` to limit number of replacements
- Great for data sanitization and text transformation

---

## Example 5: Text Splitting

**Scenario:** Split a CSV line by commas or complex delimiters.

**Simple Split:**
```bash
python regexlab.py split "," "apple,banana,cherry,date"
```

**Expected Output:**
```
[OK] Split into 4 part(s):
  1. apple
  2. banana
  3. cherry
  4. date
```

**Complex Delimiter Split:**
```bash
python regexlab.py split "[,;\s]+" "one,two;three  four"
```

**Expected Output:**
```
[OK] Split into 4 part(s):
  1. one
  2. two
  3. three
  4. four
```

**What You Learned:**
- Split text using any regex pattern
- Handle multiple delimiters with a single pattern
- Clean up data by splitting on whitespace variations

---

## Example 6: Using Flags (Case-Insensitive)

**Scenario:** Match text regardless of case.

**Without Flag (case-sensitive):**
```bash
python regexlab.py test "hello" "Hello HELLO hello"
```

**Expected Output:**
```
[OK] 1 match(es) found

Match #1:
  Position: 12-17
  Matched: 'hello'
```

**With Case-Insensitive Flag:**
```bash
python regexlab.py test "hello" "Hello HELLO hello" -i
```

**Expected Output:**
```
[OK] Pattern: hello
[OK] Flags: IGNORECASE
[OK] Test String: Hello HELLO hello
----------------------------------------------------------------------
[OK] 3 match(es) found

Match #1:
  Position: 0-5
  Matched: 'Hello'

Match #2:
  Position: 6-11
  Matched: 'HELLO'

Match #3:
  Position: 12-17
  Matched: 'hello'
```

**Available Flags:**
- `-i` / `--ignorecase` - Case-insensitive matching
- `-m` / `--multiline` - `^` and `$` match line boundaries
- `-s` / `--dotall` - `.` matches newlines too

**What You Learned:**
- Use flags to modify pattern behavior
- Multiple flags can be combined
- Essential for flexible text matching

---

## Example 7: Managing Favorites

**Scenario:** Save frequently used patterns for quick access.

**Add a Favorite:**
```bash
python regexlab.py favorite add my_phone "\d{3}-\d{3}-\d{4}" --description "US phone number"
```

**Expected Output:**
```
[OK] Added 'my_phone' to favorites
```

**List Favorites:**
```bash
python regexlab.py favorite list
```

**Expected Output:**
```
[OK] Favorite Patterns:
----------------------------------------------------------------------

my_phone (added 2026-01-24):
  Pattern: \d{3}-\d{3}-\d{4}
  Description: US phone number
```

**What You Learned:**
- Save custom patterns for reuse
- Add descriptions for documentation
- Build your personal pattern library

---

## Example 8: Viewing History

**Scenario:** Review recently tested patterns.

**Command:**
```bash
python regexlab.py history -n 5
```

**Expected Output:**
```
[OK] Last 5 Pattern(s):
----------------------------------------------------------------------

1. [2026-01-24 14:30]
   Pattern: \d{3}-\d{3}-\d{4}
   Test: Call me at 555-123-4567

2. [2026-01-24 14:25]
   Pattern: [A-Z][a-z]+
   Test: Hello World

3. [2026-01-24 14:20]
   Pattern: \d+
   Test: abc 123 def 456

...
```

**What You Learned:**
- History is automatically saved
- Last 50 patterns are retained
- Quickly find and reuse past patterns

---

## Example 9: Exporting Matches

**Scenario:** Extract all email addresses from text and save to a file.

**Export to JSON:**
```bash
python regexlab.py export "[a-z]+@[a-z]+\.[a-z]+" "Contact: john@email.com or jane@work.org" emails.json
```

**Expected Output:**
```
[OK] Exported 2 match(es) to emails.json
```

**emails.json Content:**
```json
{
  "pattern": "[a-z]+@[a-z]+\\.[a-z]+",
  "match_count": 2,
  "matches": ["john@email.com", "jane@work.org"],
  "exported": "2026-01-24T14:35:00.000000"
}
```

**Export Formats Available:**
- `--format json` (default) - Structured JSON with metadata
- `--format csv` - CSV file with header
- `--format txt` - Plain text, one match per line

**What You Learned:**
- Export matches for further processing
- Multiple formats for different use cases
- Include metadata in JSON exports

---

## Example 10: Capturing Groups

**Scenario:** Extract structured data using capturing groups.

**Command:**
```bash
python regexlab.py test "(\d{3})-(\d{3})-(\d{4})" "Phone: 555-123-4567" -g
```

**Expected Output:**
```
[OK] Pattern: (\d{3})-(\d{3})-(\d{4})
[OK] Flags: None
[OK] Test String: Phone: 555-123-4567
----------------------------------------------------------------------
[OK] 1 match(es) found

Match #1:
  Position: 7-19
  Matched: '555-123-4567'
  Groups: ('555', '123', '4567')
```

**Named Groups:**
```bash
python regexlab.py test "(?P<area>\d{3})-(?P<exchange>\d{3})-(?P<number>\d{4})" "555-123-4567" -g
```

**Expected Output:**
```
Match #1:
  Position: 0-12
  Matched: '555-123-4567'
  Groups: ('555', '123', '4567')
  Named Groups: {'area': '555', 'exchange': '123', 'number': '4567'}
```

**What You Learned:**
- Use `-g` flag to show capturing groups
- Named groups provide labeled extraction
- Essential for parsing structured data

---

## Example 11: Email Validation Workflow

**Scenario:** Complete workflow for validating emails in a contact list.

**Step 1: Test the Pattern**
```bash
python regexlab.py library test email "user@example.com"
# Verify: [OK] 1 match(es) found
```

**Step 2: Find All Emails in Text**
```bash
python regexlab.py find "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" "Contact: john@test.com, jane@work.org, invalid-email, bob@example.net"
```

**Expected Output:**
```
[OK] Found 3 match(es)
  1. john@test.com
  2. jane@work.org
  3. bob@example.net
```

**Step 3: Export Valid Emails**
```bash
python regexlab.py export "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" "Contact: john@test.com, jane@work.org, bob@example.net" valid_emails.txt --format txt
```

**Step 4: Save Pattern to Favorites**
```bash
python regexlab.py favorite add email_extract "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" --description "Extract emails from text"
```

**What You Learned:**
- Combine multiple commands for complete workflows
- Test, extract, export, and save patterns
- Build reusable validation pipelines

---

## Example 12: Log File Analysis

**Scenario:** Parse log entries to extract timestamps and error messages.

**Sample Log Line:**
```
2026-01-24 14:30:45 ERROR [main] Connection failed: timeout
```

**Extract Timestamps:**
```bash
python regexlab.py find "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}" "2026-01-24 14:30:45 ERROR [main] Connection failed"
```

**Extract Error Level:**
```bash
python regexlab.py find "(ERROR|WARN|INFO|DEBUG)" "2026-01-24 14:30:45 ERROR [main] Connection failed"
```

**Parse Complete Entry with Groups:**
```bash
python regexlab.py test "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) \[(\w+)\] (.+)" "2026-01-24 14:30:45 ERROR [main] Connection failed" -g
```

**Expected Output:**
```
Match #1:
  Position: 0-51
  Matched: '2026-01-24 14:30:45 ERROR [main] Connection failed'
  Groups: ('2026-01-24 14:30:45', 'ERROR', 'main', 'Connection failed')
```

**What You Learned:**
- Parse structured log formats
- Use groups to extract components
- Build patterns incrementally (test each part)

---

## 🎓 Tips for Effective Regex Testing

1. **Start Simple**: Test basic patterns before adding complexity
2. **Use Library**: Check if a pattern exists before writing your own
3. **Save Favorites**: Store patterns you'll use again
4. **Check History**: Don't rewrite patterns you've used before
5. **Export Results**: Save matches for analysis in other tools
6. **Use Flags**: `-i` for case-insensitive, `-g` for groups
7. **Test Edge Cases**: Empty strings, special characters, long text

---

## 📚 Additional Resources

- **README**: Full documentation → `README.md`
- **Cheat Sheet**: Quick reference → `CHEAT_SHEET.txt`
- **Integration**: Team Brain integration → `INTEGRATION_PLAN.md`
- **GitHub**: https://github.com/DonkRonk17/RegexLab

---

**Built by:** Atlas (Team Brain)  
**For:** Logan Smith / Metaphy LLC  
**Last Updated:** January 24, 2026
