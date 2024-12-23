# Introduction

Hi Ethermed crew! 👋

I am Eugene Tsuprun, and this is my code sample. I've really enjoyed the interview process so far, and I'd
be very excited about working at Ethermed.

You've requested a code sample I'm proud of. I decided to put together a new one from scratch based on a problem I made up.

tl;dr: Process clinical text without sending _everything_ to AI.

# Problem

I know that Ethermed processes clinical data and extracts some insights related to the prior auth process.

I figured a couple of pieces of data you would be interested in are:

- The CPT code(s) associated with the clinical procedures being sought.
- The ICD-10 code(s) corresponding to diagnoses relevant to a prior auth request.

I assume Ethermed has or can get a BAA with an AI provider. And it's easy enough to ask AI to just read everything and spit out the codes.

I do wonder about the cost, though. 💸

If you're processing tons of clinical text, you might not want to send every single page to AI. You might run up a huge bill and maybe brush up against the rate limits.

# Solution

I created a POC of a backend that analyzes clinical text to extract the relevant CPT and ICD-10 without sending _everything_ to AI.
Here is how it works:

1. A Web API takes in a clinical text as input.
1. We split up the text into overlapping chunks.
1. We use a the `Clinical-AI-Apollo/Medical-NER` prebuilt offline model to detect chunks containing references to clinical procedures and disorders/diseases. It's not perfect at detecting clinical concepts, but it is easy to set up, and it's good enough for filtering out text chunks that are unlikely to contain anything noteworthy for our purposes.
1. If a chunk is likely to contain references to diagnoses and procedures, we send it to AI and ask for the CPT and ICD-10 codes (only the ones likely relevant to an ongoing prior auth request).
1. We merge the results from all the chunks and save them in the database.

The processing happens in the background. `POST` a request to `/process`, and include a `document` and, optionally, a `document_id`. If you don't provide a `document_id`, we'll generate one.

When processing is done, check your results by sending a `GET` request to `/result/{document_id}`.

A few things are missing here:

- Authentication. Right now all the endpoints are wide open!!
- A BAA with OpenAI. That would be absolutely required before sending any PHI to OpenAI.
- Queueing. If the server crashes, the work in flight is lost.
- A proper database.
- A golden test set, to make sure AI is behaving the way we expect.
- Logging / error handling / observability

# Setup

Set your `OPENAI_API_KEY` in the `.env` file in the `ethermed` dir.

Poetry is a dependency management tool for Python. If you don't have it installed, follow the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

Then, run `poetry install`.

Enter the poetry-managed virtual environment with `poetry shell`.

# Start the Server

```
cd ethermed
python -m uvicorn app:app --reload
```

This will run the server on port 8000.

# Send a Request

```
./post_doc_to_api.sh sample_docs/prior_auth_letter.txt test1
```

This will `POST` a request to `http://localhost:8000/process` with the contents of `sample_docs/prior_auth_letter.txt` and a `document_id` of `test1`.

# Check the Results

```
./check_results.sh test1
```

This will `GET` the results of the processing of the document with `document_id` `test1`.

# Sample Input and Output

```
$ ./post_doc_to_api.sh sample_docs/prior_auth_letter.txt test1

----------------------------------------
Document sent for processing.
Document ID: test1
----------------------------------------
$ ./check_results.sh test1
{
  "icd10_codes": [
    "H90.3",
    "F41.1"
  ],
  "cpt_codes": [
    "92602",
    "92626",
    "69930"
  ]
}
```

```
$ ./post_doc_to_api.sh sample_docs/nonsense.txt test2

----------------------------------------
Document sent for processing.
Document ID: test2
----------------------------------------
$ ./check_results.sh test2
{
  "icd10_codes": [],
  "cpt_codes": []
}
```

# Tests

I wrote a few super basic tests of just the code that splits documents into chunks. Just to show that I know how to write tests. Run them with `pytest`.
# clinical-pipeline
