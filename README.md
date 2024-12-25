# Clinical Text Processing for ICD-10 and CPT Code Extraction

This project processes clinical text documents to extract relevant ICD-10 and CPT codes using a combination of Named Entity Recognition (NER) and the OpenAI API.

## Overview

The process involves the following steps:

1.  **Chunking:** The input document is split into smaller, overlapping chunks to manage long text effectively.
2.  **Relevance Filtering:** Each chunk is analyzed using a pre-trained NER model to identify relevant clinical entities (e.g., diseases, procedures). Chunks without significant entities are skipped.
3.  **Code Extraction:** Relevant chunks are passed to the OpenAI API (specifically, `gpt-4o-mini`) to extract ICD-10 and CPT codes based on the identified clinical entities.
4.  **Aggregation:** The extracted codes from all relevant chunks are combined and deduplicated to produce a final list of codes.

## Requirements

- Python 3.8 or higher
- `transformers` library
- `openai` library
- `dotenv` library
- An OpenAI API key (stored in a `.env` file)
- A pre-trained NER model for clinical text (specifically, `Clinical-AI-Apollo/Medical-NER` from Hugging Face)

## Installation

1.  Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```
