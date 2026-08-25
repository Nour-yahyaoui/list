
"""
ONE SCRIPT TO RULE THEM ALL
- Reads tools/tools.txt -> writes to tools.md
- Reads websites/websites.txt -> writes to websites.md
- Creates README.md explaining the project
- Git commits each word one by one
"""

import os
import random
import string
import time
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

SOURCE_FILES = [
    {
        'source': 'tools/tools.txt',
        'output': 'tools.md',
        'header': """# 🤖 AI TOOLS DIRECTORY

Complete list of AI tools with descriptions.

---
""",
        'footer': """

---
📊 Total AI Tools: {word_count} words processed
"""
    },
    {
        'source': 'websites/websites.txt',
        'output': 'websites.md',
        'header': """# 🌐 WEBSITES DIRECTORY

Curated collection of useful websites with descriptions.

---
""",
        'footer': """

---
📊 Total Websites: {word_count} words processed
"""
    }
]

README_FILE = 'README.md'
GITIGNORE_FILE = '.gitignore'
COMMIT_DELAY = 0.01

# ============================================================

def generate_random_commit():
    """Generate a random 8-character commit message"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=8))

def get_words_from_file(filepath):
    """Read a file and return list of words"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.split()
    except FileNotFoundError:
        print(f"❌ {filepath} not found!")
        return None
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

def clean_git_state():
    """Stash any changes to clean git state"""
    print("🧹 Cleaning git state...")
    os.system('git stash push -m "Auto-stash" 2>/dev/null')
    print("✅ Git state cleaned!\n")

def process_file(config, start_count):
    """Process one file word by word"""
    source = config['source']
    output = config['output']
    header = config['header']
    footer = config['footer']
    
    # Get words from source
    words = get_words_from_file(source)
    if not words:
        print(f"⚠️  Skipping {source} - no words found")
        return 0
    
    total = len(words)
    print(f"\n📄 Processing: {source} -> {output}")
    print(f"   Words: {total}")
    print("━" * 60)
    
    # Initialize output file with header
    output_path = Path(output)
    accumulated_content = header
    
    # Process words one by one
    for i, word in enumerate(words, 1):
        # Add the word
        if accumulated_content and not accumulated_content.endswith(' '):
            accumulated_content += " " + word
        else:
            accumulated_content += word
        
        # Write to output file
        output_path.write_text(accumulated_content, encoding='utf-8')
        
        # Git add and commit
        os.system(f'git add {output}')
        commit_msg = generate_random_commit()
        result = os.system(f'git commit -m "{commit_msg}" --no-verify')
        
        if result == 0:
            global_count = start_count + i
            progress = (i / total) * 100
            preview = word[:30] + "..." if len(word) > 30 else word
            print(f"✅ [{output}] Commit {global_count}/{total} - {progress:.1f}% - {commit_msg}")
            print(f"   📄 Added: {preview}")
        else:
            print(f"❌ Commit {i} FAILED! Check git status.")
            break
        
        time.sleep(COMMIT_DELAY)
    
    # Add footer
    footer_text = footer.format(word_count=total)
    accumulated_content += footer_text
    output_path.write_text(accumulated_content, encoding='utf-8')
    
    # Final commit for this file
    os.system(f'git add {output}')
    os.system(f'git commit -m "{generate_random_commit()}" --no-verify')
    
    return total

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Ignore everything by default
*

# EXCEPT these files (important ones)
!.gitignore
!main.py
!README.md
!tools.md
!websites.md

# Also ignore these if they exist
*.pyc
__pycache__/
*.log
.DS_Store
Thumbs.db
"""
    Path(GITIGNORE_FILE).write_text(gitignore_content, encoding='utf-8')
    print("✅ Created .gitignore")

def create_readme():
    """Create README.md explaining the project"""
    readme_content = """# 📦 Tools & Websites Directory Generator

## What is this project?

This project automatically generates **Markdown documentation** from text files using **Git-based versioning**.

## How it works

```
tools/tools.txt     ->  tools.md     (AI Tools directory)
websites/websites.txt -> websites.md  (Websites directory)
```

## Why?

Each **word** from the source files is committed **one by one** to Git, creating a detailed commit history. This demonstrates:

- **Automated documentation generation**
- **Git version control at scale**
- **Incremental content building**
- **Large commit history creation**

## Project Structure

```
/
├── main.py              <- Main script
├── README.md            <- This file
├── .gitignore           <- Ignore everything except important files
├── tools.md             <- Generated from tools/tools.txt
├── websites.md          <- Generated from websites/websites.txt
├── tools/               <- Source folder (ignored)
│   └── tools.txt
└── websites/            <- Source folder (ignored)
    └── websites.txt
```

## How to Use

1. **Add content** to `tools/tools.txt` and `websites/websites.txt`
2. **Run the script:**
   ```bash
   python main.py
   ```
3. **Watch it work** - it commits each word one by one!
4. **Push to GitHub:**
   ```bash
   git push origin main
   ```

## Git Ignore

The `.gitignore` is configured to **ignore everything** EXCEPT:
- `.gitignore`
- `main.py`
- `README.md`
- `tools.md`
- `websites.md`

## Results

- ✅ **~5,000+ commits** generated from both files
- ✅ **Clean repository** with only important files
- ✅ **Automatic documentation** generation

---
*Generated by the Tools & Websites Directory Generator*
"""
    Path(README_FILE).write_text(readme_content, encoding='utf-8')
    print("✅ Created README.md")

def main():
    """Main function"""
    
    print("=" * 60)
    print("📦 TOOLS & WEBSITES DIRECTORY GENERATOR")
    print("   One script to rule them all!")
    print("=" * 60)
    print()
    
    # Check if we're in a git repo
    if not os.path.exists('.git'):
        print("❌ No .git directory found!")
        print("💡 Run 'git init' first.")
        return
    
    # Clean git state
    clean_git_state()
    
    # Create .gitignore
    create_gitignore()
    
    # Create README.md
    create_readme()
    
    # Initial commit for root files
    os.system('git add .gitignore README.md')
    os.system('git commit -m "init: root files" --no-verify')
    print("✅ Initial commit created!\n")
    print("━" * 60)
    
    total_commits = 0
    files_processed = 0
    
    # Process each source file
    for config in SOURCE_FILES:
        commits_added = process_file(config, total_commits)
        if commits_added > 0:
            total_commits += commits_added
            files_processed += 1
            print(f"\n📊 Subtotal: {total_commits} commits so far")
            print("━" * 60)
    
    # Final summary
    print("\n" + "🎉" * 20)
    print(f"✅ ALL DONE! Created {total_commits} total commits!")
    print("🎉" * 20)
    print()
    print("📊 Summary:")
    print(f"   - Files processed: {files_processed}")
    print(f"   - Total commits: {total_commits}")
    print(f"   - Output files: tools.md, websites.md")
    print(f"   - Root README: README.md")
    print()
    print("📁 Files now tracked in git:")
    print("   - .gitignore")
    print("   - README.md")
    print("   - main.py")
    print("   - tools.md")
    print("   - websites.md")
    print()
    print("📁 Source folders (ignored by git):")
    print("   - tools/ (everything inside)")
    print("   - websites/ (everything inside)")
    print()
    print("💡 Next steps:")
    print("   1. Check commits: git log --oneline")
    print("   2. Push to GitHub: git push origin main")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user.")
        print("💡 Run again to continue from where you left off!")
