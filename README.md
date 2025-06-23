# ContentGenie🧞‍♂️

**AI-Powered Multi-Agent Marketing Content Studio**

**Agent Architecture Diagram**
![ContentGenie Architecture Diagram](https://i.imgur.com/example-image.png)

## Key Features ✨

- **Automated Audience Analysis** - Generates detailed customer personas from product descriptions
- **Intelligent Content Strategy** - Creates data-driven campaign plans tailored to your goals
- **Multi-Platform Copywriting** - Produces optimized content for social media, emails, and ads
- **Design Recommendations** - Suggests visual styles, color palettes, and image concepts
- **AI Image Generation** - Creates custom visuals using Google's Imagen model
- **Content Review & Scoring** - Evaluates tone, clarity, and marketing effectiveness
- **Automated Scheduling** - Generates  ready for your marketing tools
- **Google Cloud Integration** - Saves generated image to Google Cloud Storage, utilizes Google Cloud for API provisioning


## Tech Stack 🛠️

- **Core Framework**: Google Agent Development Kit (ADK)
- **AI Models**: Gemini 1.5 Pro, Imagen 3.0
- **Cloud Services**: Google Cloud Storage, Google Docs/Sheets API
- **Languages**: Python 3.10+
- **Dependencies**: Pillow, google-generativeai, google-cloud-storage

## Getting Started 🚀

### Prerequisites
- Google Cloud account with Vertex AI enabled
- Python 3.10+ installed
- Valid Google API credentials

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/ContentGenie.git
cd ContentGenie

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate.bat  # Windows
