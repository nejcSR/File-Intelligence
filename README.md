# Document Intelligence System

An AI-powered document processing system that ingests invoices, contracts, resumes, and other documents in PDF, image, Word, or text format — extracts structured data from them, flags anomalies, and stores everything in a searchable, exportable database.

Built as a portfolio project to demonstrate end-to-end system design: file parsing, OCR, AI-driven structured extraction, background task processing, and a clean review dashboard — not just a thin wrapper around an LLM API call.

<img width="1920" height="917" alt="Docint1" src="https://github.com/user-attachments/assets/cd106c39-c1b8-4118-8758-c1a9922f6ce8" />


---

## What It Does

You drop in one or more documents. The system:

1. Extracts raw text — directly from PDFs and Word docs, or via OCR for scanned documents and images
2. Sends that text to an LLM with a structured prompt, asking it to classify the document, pull out key fields, flag anomalies, and summarize it
3. Stores everything in a database
4. Displays the results in a dashboard you can search, filter, export, or delete from

It's the difference between pasting a document into a chat window once, and having a system that can process hundreds of documents reliably, consistently, and on its own schedule.

<img width="1906" height="951" alt="Docint2" src="https://github.com/user-attachments/assets/347f3108-56e8-4b08-ac72-12ca8c6faf7c" />

---

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌────────────────┐      ┌─────────────┐
│   Upload    │ ───> │   Parsing    │ ───> │  AI Extraction │ ───> │  Database   │
│  (1+ files) │      │ PDF/OCR/DOCX │      │  (Groq/Llama)  │      │  (SQLite)   │
└─────────────┘      └──────────────┘      └────────────────┘      └──────┬──────┘
                                                                            │
                                                                            v
                                                                  ┌──────────────────┐
                                                                  │   Dashboard UI    │
                                                                  │ search/filter/CSV │
                                                                  └──────────────────┘
```

**Why each layer exists:**

- **Parsing layer** — a PDF, a scanned receipt, and a Word document all need different handling before any AI ever sees them. This layer normalizes everything down to plain text first.
- **AI extraction layer** — a tightly structured prompt forces the model to return consistent JSON every time (document type, key fields, anomalies, confidence, summary), rather than freeform chat text that's unusable programmatically.
- **Background processing** — extraction and OCR are slow operations. Uploads are accepted instantly and processed in the background, so the API stays responsive even with multiple files queued at once.
- **Database layer** — results persist, so you can search and review across hundreds of documents instead of one chat session at a time.

---

## Tech Stack

- **FastAPI** — backend API and background task handling
- **SQLite** — storage for documents and extracted data
- **Groq (Llama 3.3)** — structured AI extraction
- **pdfplumber** — native PDF text extraction
- **Tesseract OCR** — text extraction from scanned documents and images
- **python-docx** — Word document parsing
- **Plain HTML/CSS/JS** — frontend, no build step required
- **Docker** — containerized for consistent deployment, Tesseract included

---

## Features

- **Multi-format support** — PDF, DOCX, TXT, and images (PNG, JPG, JPEG, WEBP, GIF, JFIF)
- **Bulk upload** — drop in multiple files at once; each is queued and processed independently with a live progress bar
- **Structured AI extraction** — document type, key fields, anomalies, and a plain-language summary, returned as consistent JSON every time
- **Anomaly flagging** — the AI is explicitly prompted to flag anything suspicious, missing, or inconsistent in the document
- **Searchable dashboard** — instant client-side search by filename, with filters for document type and confidence level
- **CSV export** — download all processed documents and their extracted data as a spreadsheet
- **Document deletion** — remove individual documents or wipe everything at once
- **Failure visibility** — if processing fails on a document, the actual error reason is stored and viewable, not just a generic "failed" status

<img width="1920" height="935" alt="Docint5" src="https://github.com/user-attachments/assets/f48a539f-dc69-40ce-8358-132a713a0b09" />


---

## Running Locally

**Requirements:** Python 3.10+, Tesseract OCR installed locally, a Groq API key

```bash
# clone the repo
git clone https://github.com/nejcSR/File-Intelligence.git
cd File-Intelligence

# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# install dependencies
pip install -r requirements.txt

# add your Groq API key
echo GROQ_API_KEY=your_key_here > .env

# run the server
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000`.

> Note: `pytesseract.pytesseract.tesseract_cmd` in `app/main.py` is set for the local Windows install path used in development. Update it to your own Tesseract path if running locally on Windows, or remove it entirely on macOS/Linux where Tesseract is typically found automatically.

---

## Running with Docker

No local Python, Tesseract, or dependency setup required — everything is built into the image.

```bash
docker build -t file-processor .
docker run -p 8000:8000 --env-file .env file-processor
```

Visit `http://127.0.0.1:8000`.

This is also how the project is deployed to Render — Render builds directly from the `Dockerfile` in this repo on every push.

<img width="1900" height="941" alt="Docint3" src="https://github.com/user-attachments/assets/7599198f-ac57-43c3-b32d-8736b1cc6d13" />


---

## Known Limitations & Next Steps

This is a portfolio project, and being upfront about its current limitations is more useful than pretending they don't exist:

- **Storage is ephemeral and shared.** The SQLite database and uploaded files live on local disk, which resets on every redeploy/restart on Render's free tier, and there's no per-user separation — everyone visiting the live demo shares the same data. Planned fix: migrate to a hosted Postgres database and add basic auth or per-session scoping.
- **No retry mechanism for failed extractions.** If a document fails (corrupted file, AI error), it's flagged but not automatically retried.
- **Single AI provider.** Currently hardcoded to Groq/Llama; no fallback if the API is unavailable.

---

## Why This Project

This was built as the third piece of a three-project portfolio, alongside a price-tracking system (scraping + AI auditing) and an email automation tool (AI-drafted responses, labeling, Gmail integration). Where those two focus on monitoring and communication automation, this project focuses on a third common business problem: turning unstructured documents into structured, actionable data — a need that spans finance, HR, and legal workflows alike.
