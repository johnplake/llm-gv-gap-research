# NotebookLM for Presentations: Access Options for OpenClaw Agents

**Research Date:** 2026-02-11  
**Purpose:** Evaluate how OpenClaw agents can access NotebookLM to create presentations

---

## 📊 NotebookLM Presentation Capabilities

### What NotebookLM Can Generate

**Slide Decks:**
- **Two formats:**
  - **Detailed Deck** - Comprehensive with full text, perfect for reading/emailing
  - **Presenter Slides** - Clean, visual slides with key talking points
- **Customization options:**
  - Length: short, default, or long
  - Language: 50+ languages supported
  - Custom prompts for style/audience/focus
- **Export:** PDF format (direct download)
- **In-app presentation mode:** Full-screen slideshow

**Additional Content Types:**
- Audio Overviews (podcasts) - MP3/MP4
- Video Overviews (9 visual styles) - MP4
- Infographics (3 orientations) - PNG
- Quizzes & Flashcards - JSON/Markdown/HTML
- Study Guides & Briefing Docs - Markdown
- Mind Maps - JSON
- Data Tables - CSV

### Generation Workflow (Web UI)

1. Upload sources (PDFs, URLs, YouTube, Google Drive, text)
2. Go to "Studio" panel
3. Select "Slide Deck"
4. Optional: Customize format, length, language, prompt
5. Generate (runs in background, takes ~10 minutes)
6. Download as PDF or present in-app

**Limitations:**
- Only exports as PDF (not PPTX natively)
- AI-generated (may contain inaccuracies)
- Requires edit access to notebook
- 18+ age restriction

---

## 🔑 Access Options for OpenClaw Agents

### Option 1: Official Enterprise API (Google Cloud) ⭐

**Availability:** Enterprise customers only (NotebookLM Enterprise)  
**Cost:** Requires Google Cloud billing + Enterprise license  
**Status:** Recently released (Nov 2025)

**What's Available:**
- ✅ Create/manage notebooks
- ✅ Add sources (URLs, files, Drive, YouTube)
- ✅ Generate audio overviews (podcasts)
- ✅ Chat/query interface
- ✅ Share notebooks programmatically
- ❓ **Slide deck generation** - Not explicitly documented yet

**API Endpoint:**
```bash
# Example: Create notebook
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://us-discoveryengine.googleapis.com/v1alpha/projects/PROJECT_NUMBER/locations/global/notebooks" \
  -d '{"title": "My Notebook"}'
```

**Documentation:**
- https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks
- https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/podcast-api

**Requirements:**
1. Google Cloud Project with billing enabled
2. NotebookLM Enterprise license
3. IAM permissions configured
4. Service account or OAuth token

**Pros:**
- ✅ Official Google support
- ✅ Enterprise-grade reliability
- ✅ Full integration with Google Cloud
- ✅ CMEK support for security
- ✅ Audit logging

**Cons:**
- ❌ Enterprise-only (not available for free/consumer accounts)
- ❌ Requires Google Cloud setup & billing
- ❌ May not support all features yet (slide decks unclear)
- ❌ More complex authentication

---

### Option 2: Unofficial Python API (notebooklm-py) ⭐⭐⭐

**Availability:** Open source, works with consumer accounts  
**Cost:** Free (uses your NotebookLM account)  
**Status:** Actively maintained

**GitHub:** https://github.com/teng-lin/notebooklm-py  
**PyPI:** https://pypi.org/project/notebooklm-py/

**What's Available:**
- ✅ **All notebook operations** (create, list, rename, delete)
- ✅ **All source types** (URLs, YouTube, files, Drive, text)
- ✅ **Chat interface** with history
- ✅ **ALL content generation types:**
  - ✅ **Slide decks** (detailed/presenter, PDF download)
  - ✅ Audio overviews (MP3/MP4)
  - ✅ Video overviews (9 styles, MP4)
  - ✅ Quizzes & flashcards (JSON/Markdown/HTML export)
  - ✅ Infographics (PNG)
  - ✅ Mind maps (JSON)
  - ✅ Data tables (CSV)
- ✅ **Beyond web UI:** Batch downloads, structured exports
- ✅ **Web & Drive research** with auto-import

**Installation:**
```bash
# Basic
pip install notebooklm-py

# With browser login support (first-time setup)
pip install "notebooklm-py[browser]"
playwright install chromium
```

**Usage Example (Slide Deck):**
```python
import asyncio
from notebooklm import NotebookLMClient

async def create_presentation():
    async with await NotebookLMClient.from_storage() as client:
        # Create notebook and add sources
        nb = await client.notebooks.create("V2G Research Presentation")
        
        # Add sources
        await client.sources.add_url(
            nb.id, 
            "https://github.com/johnplake/llm-gv-gap-research",
            wait=True
        )
        await client.sources.add_file(
            nb.id,
            "/path/to/v2g-papers-final.md",
            wait=True
        )
        
        # Generate slide deck
        status = await client.artifacts.generate_slide_deck(
            nb.id,
            instructions="Create presenter slides for ML researchers, bold style",
            format="presenter",  # or "detailed"
            length="default",
            language="en"
        )
        
        # Wait for completion
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        
        # Download as PDF
        await client.artifacts.download_slide_deck(nb.id, "v2g-presentation.pdf")
        
        print("Presentation created: v2g-presentation.pdf")

asyncio.run(create_presentation())
```

**CLI Example:**
```bash
# One-time login
notebooklm login

# Create notebook and add sources
notebooklm create "V2G Presentation"
notebooklm use <notebook_id>
notebooklm source add "https://github.com/johnplake/llm-gv-gap-research"
notebooklm source add "./v2g-papers-final.md"

# Generate slide deck
notebooklm generate slide-deck \
  --format presenter \
  --length default \
  "Create slides for ML researchers with bold style" \
  --wait

# Download
notebooklm download slide-deck ./v2g-slides.pdf
```

**Authentication:**
- Uses browser-based login (Playwright)
- Stores credentials securely in `~/.notebooklm/`
- Cookies persist across sessions
- Works with any NotebookLM account (consumer or enterprise)

**Pros:**
- ✅ **Works with free NotebookLM accounts**
- ✅ **Full slide deck generation support**
- ✅ Easy Python API + CLI
- ✅ All features supported (beyond web UI)
- ✅ Active development, good documentation
- ✅ Open source (MIT license)
- ✅ Can be integrated into OpenClaw tools

**Cons:**
- ⚠️ **Unofficial** - uses undocumented Google APIs
- ⚠️ May break if Google changes internal endpoints
- ⚠️ Rate limits apply (heavy usage may be throttled)
- ⚠️ Not suitable for critical production systems
- ⚠️ Requires browser for initial auth

**Stability Warning:**
> This library uses undocumented Google APIs that can change without notice.
> Best for prototypes, research, and personal projects.

---

### Option 3: AutoContent API (Third-Party Service) 💰

**Availability:** Commercial service  
**Cost:** Paid API (pricing not disclosed)  
**Website:** https://autocontentapi.com

**What's Available:**
- ✅ NotebookLM-style content generation
- ✅ Access to restricted websites (news portals)
- ✅ Social media integration (Reddit, X/Twitter)
- ✅ Video creation with AI avatars
- ✅ Deep research reports
- ✅ Automated workflows

**API Approach:**
- Cloud-based automation service
- REST API endpoints
- Similar output to NotebookLM
- Additional features beyond NotebookLM

**Pros:**
- ✅ More features than NotebookLM (social media, restricted sites)
- ✅ Designed for programmatic access
- ✅ Potential for more reliability (managed service)

**Cons:**
- ❌ **Paid service** (cost unknown)
- ❌ Not actually NotebookLM (mimic)
- ❌ Unclear if slide decks specifically supported
- ❌ Less transparent than open source
- ❌ Vendor lock-in

---

### Option 4: Manual/Browser Automation 🤖

**Approach:** Use browser automation (Playwright/Selenium) to control NotebookLM web UI

**Feasibility:**
- Technically possible (like notebooklm-py does for auth)
- Would require reverse-engineering web UI interactions
- Fragile (breaks when UI changes)

**Pros:**
- ✅ Works with any account
- ✅ No API needed

**Cons:**
- ❌ Very fragile and maintenance-heavy
- ❌ Slow (real browser overhead)
- ❌ Complex error handling
- ❌ **notebooklm-py already does this better**

**Verdict:** Not recommended - use notebooklm-py instead

---

## 🎯 Recommendation for OpenClaw Agents

### Best Option: notebooklm-py (Option 2) ⭐⭐⭐

**Why:**
1. ✅ **Works with free NotebookLM accounts** (no enterprise license needed)
2. ✅ **Full slide deck support** with PDF export
3. ✅ **Easy integration** - Python API fits OpenClaw's architecture
4. ✅ **Active maintenance** and good documentation
5. ✅ **All features** including beyond-web-UI capabilities
6. ✅ **Open source** - can inspect/modify if needed

**Integration Plan:**

### Step 1: Install & Setup
```bash
# In workspace (persists)
cd ~/.openclaw/workspace
pip install "notebooklm-py[browser]" --target ./python-libs
playwright install chromium

# Or add to requirements
echo "notebooklm-py[browser]" >> requirements.txt
```

### Step 2: Create OpenClaw Tool

Create a new tool in `~/.openclaw/workspace/bin/notebooklm-tool.py`:

```python
#!/usr/bin/env python3
"""
OpenClaw tool for NotebookLM presentation generation.
Usage: notebooklm-tool.py create-slides <sources...> --output slides.pdf
"""

import asyncio
import sys
from pathlib import Path
from notebooklm import NotebookLMClient

async def create_slides(sources, output_path, instructions=None):
    """Create a slide deck from sources."""
    async with await NotebookLMClient.from_storage() as client:
        # Create notebook
        nb = await client.notebooks.create("OpenClaw Presentation")
        
        # Add sources
        for source in sources:
            if source.startswith(('http://', 'https://')):
                await client.sources.add_url(nb.id, source, wait=True)
            elif Path(source).exists():
                await client.sources.add_file(nb.id, source, wait=True)
            else:
                print(f"Skipping invalid source: {source}")
        
        # Generate slide deck
        status = await client.artifacts.generate_slide_deck(
            nb.id,
            instructions=instructions or "Professional presentation",
            format="presenter",
            length="default"
        )
        
        # Wait and download
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        await client.artifacts.download_slide_deck(nb.id, output_path)
        
        print(f"✅ Presentation saved: {output_path}")
        return output_path

if __name__ == "__main__":
    # Parse args and run
    # (simplified - add argparse for production)
    asyncio.run(create_slides(sys.argv[1:-1], sys.argv[-1]))
```

### Step 3: Usage in OpenClaw

```bash
# From exec tool
exec --command="~/bin/notebooklm-tool.py create-slides \
  https://github.com/johnplake/llm-gv-gap-research \
  ./v2g-papers-final.md \
  --output ./v2g-presentation.pdf"

# Or directly
notebooklm create "V2G Talk"
notebooklm source add ./v2g-papers-final.md
notebooklm generate slide-deck "Presentation for ML conference" --wait
notebooklm download slide-deck ./slides.pdf
```

### Step 4: Convert PDF to PPTX (Optional)

If you need PPTX instead of PDF:

```bash
# Option A: Upload to Google Slides, export as PPTX
# (notebooklm-py doesn't support this directly yet)

# Option B: Use pdf2pptx converter
pip install pdf2pptx
pdf2pptx slides.pdf slides.pptx

# Option C: Open PDF in Google Slides via Drive API
# Then export as PPTX using gog CLI
```

---

## 🔄 Alternative: Enterprise API (If Available)

If you have Google Cloud Enterprise:

```bash
# Set up gcloud auth
gcloud auth application-default login

# Create notebook
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://us-discoveryengine.googleapis.com/v1alpha/projects/PROJECT_NUMBER/locations/global/notebooks" \
  -d '{"title": "V2G Presentation"}'

# Add sources, generate content via API
# (check latest documentation for slide deck endpoints)
```

**Note:** Enterprise API documentation doesn't explicitly show slide deck generation yet. May need to wait for full feature parity.

---

## 📝 Practical Considerations

### Rate Limits
- **notebooklm-py:** Subject to NotebookLM's internal rate limits
  - Conservative usage recommended
  - Add delays between operations
  - Monitor for errors

### Generation Time
- Slide decks take **~10 minutes** to generate
- Other formats vary:
  - Audio: 5-15 minutes
  - Video: 10-20 minutes
  - Quizzes/flashcards: 2-5 minutes

### Quality Control
- AI-generated content may have inaccuracies
- Always review before sharing
- Customize instructions for better results
- Iterate if needed

### Storage & Cleanup
- Notebooks accumulate over time
- Implement cleanup routines:
```python
# List and delete old notebooks
notebooks = await client.notebooks.list_recently_viewed()
for nb in notebooks:
    if should_delete(nb):  # your logic
        await client.notebooks.delete(nb.id)
```

---

## 🚀 Implementation Roadmap

### Phase 1: Basic Setup (Day 1)
1. Install notebooklm-py in workspace
2. Run `notebooklm login` to authenticate
3. Test basic operations (create, add sources, generate)

### Phase 2: Tool Integration (Day 2-3)
1. Create wrapper script/tool
2. Test with V2G papers
3. Verify PDF output quality
4. Document workflow in TOOLS.md

### Phase 3: Automation (Week 2)
1. Create reusable functions
2. Add error handling
3. Implement cleanup routines
4. Consider caching/deduplication

### Phase 4: Advanced Features (Future)
1. Batch processing
2. Template management
3. Style customization
4. Multi-format export

---

## 📚 Resources

**notebooklm-py:**
- GitHub: https://github.com/teng-lin/notebooklm-py
- Documentation: In repo (`docs/` folder)
- CLI Reference: https://github.com/teng-lin/notebooklm-py/blob/main/docs/cli-reference.md
- Python API: https://github.com/teng-lin/notebooklm-py/blob/main/docs/python-api.md

**Official NotebookLM:**
- Enterprise API: https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks
- Slide Deck Help: https://support.google.com/notebooklm/answer/16757456
- Main site: https://notebooklm.google.com

**Other Options:**
- AutoContent API: https://autocontentapi.com

---

## ⚠️ Important Notes

1. **Unofficial API Risk:** notebooklm-py uses undocumented APIs that may break
2. **Rate Limiting:** Be conservative with API calls
3. **Authentication:** Initial browser login required (one-time)
4. **Export Format:** Native output is PDF (not PPTX)
5. **Generation Time:** 10+ minutes per slide deck
6. **Quality:** AI-generated, always review output

---

## ✅ Action Items

1. **Install notebooklm-py** in OpenClaw workspace
2. **Run initial authentication** (`notebooklm login`)
3. **Test slide generation** with V2G papers
4. **Document workflow** in TOOLS.md
5. **Create wrapper tool** for easy OpenClaw access

---

**Summary:** Use **notebooklm-py (Option 2)** for OpenClaw agent access to NotebookLM presentations. It provides full functionality including slide deck generation with PDF export, works with free accounts, and integrates easily into OpenClaw's Python/CLI workflow.
