#!/usr/bin/env python3
"""
RegexLab - Interactive Regex Tester and Pattern Library
A comprehensive CLI tool for testing, explaining, and managing regex patterns.

Author: Logan Smith / Metaphy LLC
License: MIT
Version: 1.0.0
"""

import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class RegexLab:
    """Main RegexLab class for regex testing and pattern management"""
    
    # Common regex patterns library
    PATTERN_LIBRARY = {
        "email": {
            "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "description": "Standard email address format",
            "example": "user@example.com"
        },
        "url": {
            "pattern": r"^https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$",
            "description": "HTTP/HTTPS URL",
            "example": "https://example.com/path"
        },
        "phone_us": {
            "pattern": r"^\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$",
            "description": "US phone number (various formats)",
            "example": "(555) 123-4567"
        },
        "ip_address": {
            "pattern": r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            "description": "IPv4 address",
            "example": "192.168.1.1"
        },
        "date_iso": {
            "pattern": r"^\d{4}-\d{2}-\d{2}$",
            "description": "ISO date format (YYYY-MM-DD)",
            "example": "2026-01-15"
        },
        "time_24h": {
            "pattern": r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
            "description": "24-hour time format (HH:MM)",
            "example": "14:30"
        },
        "hex_color": {
            "pattern": r"^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$",
            "description": "Hexadecimal color code",
            "example": "#FF5733"
        },
        "username": {
            "pattern": r"^[a-zA-Z0-9_-]{3,16}$",
            "description": "Username (3-16 chars, alphanumeric, underscore, hyphen)",
            "example": "user_name-123"
        },
        "password_strong": {
            "pattern": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            "description": "Strong password (8+ chars, upper, lower, digit, special)",
            "example": "Pass@word123"
        },
        "credit_card": {
            "pattern": r"^\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}$",
            "description": "Credit card number (with optional separators)",
            "example": "1234-5678-9012-3456"
        },
        "ssn": {
            "pattern": r"^\d{3}-\d{2}-\d{4}$",
            "description": "US Social Security Number",
            "example": "123-45-6789"
        },
        "zip_code_us": {
            "pattern": r"^\d{5}(?:-\d{4})?$",
            "description": "US ZIP code (5 or 9 digits)",
            "example": "12345-6789"
        }
    }
    
    def __init__(self):
        self.config_dir = Path.home() / ".regexlab"
        self.history_file = self.config_dir / "history.json"
        self.favorites_file = self.config_dir / "favorites.json"
        self._ensure_config()
    
    def _ensure_config(self):
        """Ensure configuration directory and files exist"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.history_file.exists():
            self.history_file.write_text(json.dumps([], indent=2))
        if not self.favorites_file.exists():
            self.favorites_file.write_text(json.dumps({}, indent=2))
    
    def _load_history(self) -> List[Dict]:
        """Load pattern history"""
        return json.loads(self.history_file.read_text())
    
    def _save_history(self, history: List[Dict]):
        """Save pattern history"""
        # Keep last 50 entries
        history = history[-50:]
        self.history_file.write_text(json.dumps(history, indent=2))
    
    def _load_favorites(self) -> Dict:
        """Load favorite patterns"""
        return json.loads(self.favorites_file.read_text())
    
    def _save_favorites(self, favorites: Dict):
        """Save favorite patterns"""
        self.favorites_file.write_text(json.dumps(favorites, indent=2))
    
    def _add_to_history(self, pattern: str, test_string: str, flags: int):
        """Add pattern to history"""
        history = self._load_history()
        entry = {
            "pattern": pattern,
            "test_string": test_string[:100],  # Truncate for storage
            "flags": flags,
            "timestamp": datetime.now().isoformat()
        }
        history.append(entry)
        self._save_history(history)
    
    def test_pattern(self, pattern: str, test_string: str, flags: int = 0, show_groups: bool = False):
        """Test a regex pattern against a string"""
        try:
            compiled_pattern = re.compile(pattern, flags)
            matches = list(compiled_pattern.finditer(test_string))
            
            print(f"\n[OK] Pattern: {pattern}")
            print(f"[OK] Flags: {self._flags_to_string(flags)}")
            print(f"[OK] Test String: {test_string[:100]}{'...' if len(test_string) > 100 else ''}")
            print("-" * 70)
            
            if matches:
                print(f"[OK] {len(matches)} match(es) found\n")
                
                for i, match in enumerate(matches, 1):
                    print(f"Match #{i}:")
                    print(f"  Position: {match.start()}-{match.end()}")
                    print(f"  Matched: '{match.group()}'")
                    
                    if show_groups and match.groups():
                        print(f"  Groups: {match.groups()}")
                        if match.groupdict():
                            print(f"  Named Groups: {match.groupdict()}")
                    print()
                
                # Highlight matches in original string
                self._highlight_matches(test_string, matches)
            else:
                print("[X] No matches found")
            
            # Add to history
            self._add_to_history(pattern, test_string, flags)
            
        except re.error as e:
            print(f"\n[X] Invalid regex pattern: {e}")
        except Exception as e:
            print(f"\n[X] Error: {e}")
    
    def _highlight_matches(self, text: str, matches: List):
        """Highlight matched text in the original string"""
        print("Highlighted text:")
        
        result = []
        last_end = 0
        
        for match in matches:
            # Add text before match
            result.append(text[last_end:match.start()])
            # Add highlighted match
            result.append(f">>>{text[match.start():match.end()]}<<<")
            last_end = match.end()
        
        # Add remaining text
        result.append(text[last_end:])
        
        highlighted = ''.join(result)
        # Truncate if too long
        if len(highlighted) > 200:
            highlighted = highlighted[:197] + "..."
        
        print(f"  {highlighted}\n")
    
    def _flags_to_string(self, flags: int) -> str:
        """Convert regex flags to readable string"""
        flag_names = []
        if flags & re.IGNORECASE:
            flag_names.append("IGNORECASE")
        if flags & re.MULTILINE:
            flag_names.append("MULTILINE")
        if flags & re.DOTALL:
            flag_names.append("DOTALL")
        if flags & re.UNICODE:
            flag_names.append("UNICODE")
        return ", ".join(flag_names) if flag_names else "None"
    
    def list_library(self):
        """List all patterns in the built-in library"""
        print("\n[OK] RegexLab Pattern Library:")
        print("-" * 70)
        
        for name, info in sorted(self.PATTERN_LIBRARY.items()):
            print(f"\n{name}:")
            print(f"  Pattern: {info['pattern']}")
            print(f"  Description: {info['description']}")
            print(f"  Example: {info['example']}")
    
    def get_library_pattern(self, name: str) -> Optional[str]:
        """Get a pattern from the library"""
        if name in self.PATTERN_LIBRARY:
            return self.PATTERN_LIBRARY[name]["pattern"]
        return None
    
    def test_library_pattern(self, name: str, test_string: str):
        """Test a pattern from the library"""
        pattern = self.get_library_pattern(name)
        if pattern:
            print(f"[OK] Testing library pattern: {name}")
            self.test_pattern(pattern, test_string)
        else:
            print(f"[X] Pattern '{name}' not found in library")
            print("Use 'regexlab library list' to see available patterns")
    
    def find_all(self, pattern: str, text: str, flags: int = 0) -> List[str]:
        """Find all matches and return them"""
        try:
            compiled_pattern = re.compile(pattern, flags)
            matches = compiled_pattern.findall(text)
            
            print(f"\n[OK] Found {len(matches)} match(es)")
            for i, match in enumerate(matches, 1):
                print(f"  {i}. {match}")
            
            return matches
        except re.error as e:
            print(f"[X] Invalid regex pattern: {e}")
            return []
    
    def replace_pattern(self, pattern: str, replacement: str, text: str, 
                       flags: int = 0, max_count: int = 0):
        """Replace matches with replacement string"""
        try:
            compiled_pattern = re.compile(pattern, flags)
            
            # Show preview
            result = compiled_pattern.sub(replacement, text, count=max_count)
            match_count = len(compiled_pattern.findall(text))
            actual_replacements = min(match_count, max_count) if max_count > 0 else match_count
            
            print(f"\n[OK] Would replace {actual_replacements} occurrence(s)")
            print("\nOriginal:")
            print(f"  {text[:200]}{'...' if len(text) > 200 else ''}")
            print("\nResult:")
            print(f"  {result[:200]}{'...' if len(result) > 200 else ''}")
            
            return result
        except re.error as e:
            print(f"[X] Invalid regex pattern: {e}")
            return text
    
    def split_text(self, pattern: str, text: str, flags: int = 0, max_split: int = 0):
        """Split text using regex pattern"""
        try:
            compiled_pattern = re.compile(pattern, flags)
            parts = compiled_pattern.split(text, maxsplit=max_split)
            
            print(f"\n[OK] Split into {len(parts)} part(s):")
            for i, part in enumerate(parts, 1):
                display_part = part[:100] + "..." if len(part) > 100 else part
                print(f"  {i}. {display_part}")
            
            return parts
        except re.error as e:
            print(f"[X] Invalid regex pattern: {e}")
            return [text]
    
    def show_history(self, count: int = 10):
        """Show pattern history"""
        history = self._load_history()
        
        if not history:
            print("\n[X] No history found")
            return
        
        print(f"\n[OK] Last {min(count, len(history))} Pattern(s):")
        print("-" * 70)
        
        for i, entry in enumerate(reversed(history[-count:]), 1):
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
            print(f"\n{i}. [{timestamp}]")
            print(f"   Pattern: {entry['pattern']}")
            print(f"   Test: {entry['test_string'][:80]}{'...' if len(entry['test_string']) > 80 else ''}")
    
    def add_favorite(self, name: str, pattern: str, description: str = ""):
        """Add pattern to favorites"""
        favorites = self._load_favorites()
        favorites[name] = {
            "pattern": pattern,
            "description": description,
            "created": datetime.now().isoformat()
        }
        self._save_favorites(favorites)
        print(f"[OK] Added '{name}' to favorites")
    
    def list_favorites(self):
        """List favorite patterns"""
        favorites = self._load_favorites()
        
        if not favorites:
            print("\n[X] No favorites found")
            return
        
        print("\n[OK] Favorite Patterns:")
        print("-" * 70)
        
        for name, info in sorted(favorites.items()):
            created = datetime.fromisoformat(info["created"]).strftime("%Y-%m-%d")
            print(f"\n{name} (added {created}):")
            print(f"  Pattern: {info['pattern']}")
            if info.get("description"):
                print(f"  Description: {info['description']}")
    
    def export_matches(self, pattern: str, text: str, output_file: str, format: str = "json"):
        """Export matches to file"""
        try:
            compiled_pattern = re.compile(pattern)
            matches = [match.group() for match in compiled_pattern.finditer(text)]
            
            output_path = Path(output_file)
            
            if format == "json":
                data = {
                    "pattern": pattern,
                    "match_count": len(matches),
                    "matches": matches,
                    "exported": datetime.now().isoformat()
                }
                output_path.write_text(json.dumps(data, indent=2))
            elif format == "csv":
                import csv
                with open(output_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Match"])
                    for match in matches:
                        writer.writerow([match])
            elif format == "txt":
                output_path.write_text('\n'.join(matches))
            
            print(f"[OK] Exported {len(matches)} match(es) to {output_file}")
            
        except Exception as e:
            print(f"[X] Export failed: {e}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="RegexLab - Interactive Regex Tester and Pattern Library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  regexlab test "\\d+" "abc 123 def 456"           # Test pattern
  regexlab test "\\d+" "abc 123" -i                 # Case-insensitive
  regexlab test "^\\w+@\\w+\\.\\w+$" "test@mail.com" -g  # Show groups
  regexlab library list                             # Show pattern library
  regexlab library test email "user@example.com"    # Test library pattern
  regexlab find "\\d+" "abc 123 def 456"           # Find all matches
  regexlab replace "\\d+" "X" "abc 123 def 456"    # Replace matches
  regexlab history                                  # Show pattern history
  regexlab favorite add mypattern "\\d{3}"          # Save favorite
  
For more information, visit: https://github.com/DonkRonk17/RegexLab
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test a regex pattern')
    test_parser.add_argument('pattern', help='Regex pattern')
    test_parser.add_argument('text', help='Text to test against')
    test_parser.add_argument('-i', '--ignorecase', action='store_true', help='Case-insensitive')
    test_parser.add_argument('-m', '--multiline', action='store_true', help='Multiline mode')
    test_parser.add_argument('-s', '--dotall', action='store_true', help='Dot matches all (including newlines)')
    test_parser.add_argument('-g', '--groups', action='store_true', help='Show capturing groups')
    
    # Library commands
    library_parser = subparsers.add_parser('library', help='Access pattern library')
    library_sub = library_parser.add_subparsers(dest='subcommand')
    
    library_list = library_sub.add_parser('list', help='List all library patterns')
    
    library_test = library_sub.add_parser('test', help='Test a library pattern')
    library_test.add_argument('name', help='Pattern name from library')
    library_test.add_argument('text', help='Text to test')
    
    # Find command
    find_parser = subparsers.add_parser('find', help='Find all matches')
    find_parser.add_argument('pattern', help='Regex pattern')
    find_parser.add_argument('text', help='Text to search')
    find_parser.add_argument('-i', '--ignorecase', action='store_true', help='Case-insensitive')
    
    # Replace command
    replace_parser = subparsers.add_parser('replace', help='Replace matches')
    replace_parser.add_argument('pattern', help='Regex pattern')
    replace_parser.add_argument('replacement', help='Replacement string')
    replace_parser.add_argument('text', help='Text to modify')
    replace_parser.add_argument('-i', '--ignorecase', action='store_true', help='Case-insensitive')
    replace_parser.add_argument('-c', '--count', type=int, default=0, help='Max replacements (0=all)')
    
    # Split command
    split_parser = subparsers.add_parser('split', help='Split text by pattern')
    split_parser.add_argument('pattern', help='Regex pattern')
    split_parser.add_argument('text', help='Text to split')
    split_parser.add_argument('-i', '--ignorecase', action='store_true', help='Case-insensitive')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show pattern history')
    history_parser.add_argument('-n', '--count', type=int, default=10, help='Number of entries')
    
    # Favorite commands
    favorite_parser = subparsers.add_parser('favorite', help='Manage favorite patterns')
    favorite_sub = favorite_parser.add_subparsers(dest='subcommand')
    
    favorite_add = favorite_sub.add_parser('add', help='Add favorite')
    favorite_add.add_argument('name', help='Favorite name')
    favorite_add.add_argument('pattern', help='Regex pattern')
    favorite_add.add_argument('--description', default='', help='Pattern description')
    
    favorite_list = favorite_sub.add_parser('list', help='List favorites')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export matches to file')
    export_parser.add_argument('pattern', help='Regex pattern')
    export_parser.add_argument('text', help='Text to search')
    export_parser.add_argument('output', help='Output file path')
    export_parser.add_argument('-f', '--format', choices=['json', 'csv', 'txt'], 
                              default='json', help='Output format')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    lab = RegexLab()
    
    try:
        if args.command == 'test':
            flags = 0
            if args.ignorecase:
                flags |= re.IGNORECASE
            if args.multiline:
                flags |= re.MULTILINE
            if args.dotall:
                flags |= re.DOTALL
            
            lab.test_pattern(args.pattern, args.text, flags, args.groups)
            
        elif args.command == 'library':
            if args.subcommand == 'list':
                lab.list_library()
            elif args.subcommand == 'test':
                lab.test_library_pattern(args.name, args.text)
                
        elif args.command == 'find':
            flags = re.IGNORECASE if args.ignorecase else 0
            lab.find_all(args.pattern, args.text, flags)
            
        elif args.command == 'replace':
            flags = re.IGNORECASE if args.ignorecase else 0
            lab.replace_pattern(args.pattern, args.replacement, args.text, flags, args.count)
            
        elif args.command == 'split':
            flags = re.IGNORECASE if args.ignorecase else 0
            lab.split_text(args.pattern, args.text, flags)
            
        elif args.command == 'history':
            lab.show_history(args.count)
            
        elif args.command == 'favorite':
            if args.subcommand == 'add':
                lab.add_favorite(args.name, args.pattern, args.description)
            elif args.subcommand == 'list':
                lab.list_favorites()
                
        elif args.command == 'export':
            lab.export_matches(args.pattern, args.text, args.output, args.format)
            
    except KeyboardInterrupt:
        print("\n\n[X] Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[X] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
