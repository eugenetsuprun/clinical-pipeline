# Clinical Text Processing for ICD-10 and CPT Code Extraction

This is an example of how to not send everything to AI. Even though AI is so great, running up a huge bill is not. So, we use a simple NER model to filter out the text that is not relevant before sending it to the AI.

## Overview

The process involves the following steps:

1.  **Chop it up:** We split the input text into is split into smaller, overlapping chunks to manage long text effectively.
2.  **Find the good stuff:** We analyze each chunk using a pre-trained NER model to identify relevant clinical entities (e.g., diseases, procedures). If we don't find any entities, we discard the chunk.
3.  **Ask AI:** We send the relevant chunks to the OpenAI API to extract ICD-10 and CPT codes based on the identified clinical entities.

## Setup

Set your `OPENAI_API_KEY` in the `.env` file in the `clinical-pipeline` dir.

Poetry is a dependency management tool for Python. If you don't have it installed, follow the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

Then, run `poetry install`.

Enter the poetry-managed virtual environment with `poetry shell`.

## Usage

# Sample Input and Output

```
$ cd clinical-pipeline
$ python process.py sample_docs/prior_auth_letter.txt

Relevant THERAPEUTIC_PROCEDURE found: Cochlear Implantation  0.73
Relevant DIAGNOSTIC_PROCEDURE found: le thresholds  0.54
Relevant THERAPEUTIC_PROCEDURE found: device implantation  0.51
Relevant THERAPEUTIC_PROCEDURE found: sound processor  0.47
ICD-10 Codes: ['F41.1', 'H90.3']
CPT Codes: ['69930', '92602', '92626']
```
