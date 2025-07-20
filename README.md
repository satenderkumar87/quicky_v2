
# 🧠 AI-Powered UI Generator

This project converts **UI screenshots and design descriptions** into **production-ready ReactJS UIs** using AI. The system uses OpenAI for layout reasoning, component generation, and professional UI assumptions when input is incomplete.

---

## 🚀 Features

- 🖼️ Image-to-Layout Extraction from one or more UI screenshots
- 🧠 OpenAI LLM Orchestration (GPT-4 / GPT-3.5)
- ⚛️ Code Generation (ReactJS + TailwindCSS + Radix UI)
- 🌐 Local Hosting with Vite Dev Server
- 🔀 Assumption-based UI Completion with professional layouting
- 👁️ Preview of all generated screens, even if unrelated

---

## 📁 Folder Structure

```
ai-ui-generator/
│
├── agent/
│   ├── vision.py             # Extract UI layout from images
│   ├── orchestrator.py       # LLM-based layout-to-code generation
│   ├── codegen.py            # Convert layout JSON to React components
│   └── builder.py            # Coordinates multi-file input workflow
│
├── templates/
│   └── react_component.jinja # HTML/JSX template
│
├── input/
│   ├── screen1.png
│   ├── screen2.jpg
│   ├── ...
│   └── project_description.txt  # Design and functionality intent
│
├── generated_project/        # Final React app ready to preview
│
├── main.py                   # Entrypoint script
└── requirements.txt
```

---

## 📸 Input Requirements

- **Screenshots**: One or more `.png`, `.jpg`, or `.jpeg` files in the `input/` directory.
- **Project Description**: `project_description.txt` describing the project’s goals, target audience, and any known design/system requirements.

> 📌 If some screens are unrelated or minimal in detail, the LLM will assume relationships and generate consistent, professional UI screens.

---

## 🤖 How It Works

1. **Image Parsing** (`vision.py`)
   - Detect layout blocks in multiple images using YOLOv8 / LayoutParser.
   - OCR (PaddleOCR/Tesseract) extracts any visible text.

2. **Layout JSON Generation**
   - All detected UI elements from each screen are converted into layout JSON.
   - Screens are treated independently if no link is found; otherwise, relationships are inferred.

3. **AI Orchestration** (`orchestrator.py`)
   - Sends layout + description to OpenAI.
   - Prompts guide the model to generate:
     - JSX/Tailwind for each screen
     - Radix UI components
     - Routing and reusable components
     - Professional assumptions to fill missing context

4. **Code Generation** (`codegen.py`)
   - Each screen is compiled into a full-page React component.
   - Output includes routing, reusable layouts, and responsive design.

5. **Hosting** (`vite`)
   - Final app is served locally with Vite dev server.
   - Navigate between screens using a pre-built navigation menu.

---

## 🧰 Technologies Used

| Area              | Tech Used                                  |
|-------------------|---------------------------------------------|
| AI / LLM          | OpenAI GPT-4 / GPT-3.5                      |
| Image Processing  | OpenCV, PaddleOCR, LayoutParser             |
| Code Generation   | Python, Jinja2                              |
| Frontend          | ReactJS, TailwindCSS, Radix UI, Vite        |
| Orchestration     | Custom Python agent with OpenAI SDK         |

---

## ⚙️ Prerequisites

- Python 3.9+
- Node.js (for Vite dev server)
- OpenAI API Key
- Pip packages (see `requirements.txt`)

---

## 🧪 Example Prompt (used by the agent)

```plaintext
You are a frontend engineer. Generate production-ready ReactJS components using Tailwind CSS and Radix UI from the following layout and design context:

Layout JSON (screen 1):
[
  { "type": "input", "label": "Email" },
  { "type": "button", "text": "Subscribe" }
]

Layout JSON (screen 2):
[
  { "type": "navbar", "items": ["Home", "Login", "Dashboard"] },
  { "type": "card", "title": "User Profile" }
]

Project Description:
"A responsive web app for newsletter signup and profile viewing. Should be minimal, professional, mobile-first, using Radix UI and Tailwind."
```

---

## 🖥️ Run Locally

```bash
git clone https://github.com/yourname/ai-ui-generator
cd ai-ui-generator

# Install Python packages
pip install -r requirements.txt

# Set your OpenAI key
export OPENAI_API_KEY=your-key-here

# Run the generator
python main.py

# Start local Vite dev server (after generation)
cd generated_project
npm install
npm run dev
```

---

## 🧩 Best Practices

- Group images by feature/page to keep visual coherence
- Keep filenames descriptive (e.g., `login_screen.png`, `profile_view.jpg`)
- Use concise, goal-driven descriptions to guide the LLM
- Define preferred stack (e.g., **Radix UI**, **Chakra**, or **Tailwind**) in `project_description.txt`
- Ensure generated components follow accessibility standards (Radix is ARIA-friendly)
- Use Tailwind utility classes for rapid responsive design
- Review and customize Jinja2 templates to fit project conventions

---

## 📌 Future Enhancements

- [ ] Add visual editor for post-generation tweaks
- [ ] Multi-step form recognition
- [ ] Figma API integration
- [ ] Export to other frameworks (Vue, Angular)

---

## 📄 License

MIT
