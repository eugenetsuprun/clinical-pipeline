import argparse
import json

from transformers import pipeline
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

pipe = pipeline(
    "token-classification",
    model="Clinical-AI-Apollo/Medical-NER",
    aggregation_strategy="simple",
)


def split_into_chunks(text, chunk_size=1000, overlap=100):
    """Splits a string into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def is_relevant(clinical_text_chunk: str) -> bool:
    """Determines if a text chunk is relevant based on NER."""
    result = pipe(clinical_text_chunk)
    for entity in result:
        if entity["entity_group"] in [
            "DISEASE_DISORDER",
            "THERAPEUTIC_PROCEDURE",
            "DIAGNOSTIC_PROCEDURE",
        ]:
            if entity["score"] > 0.4:  # somewhat arbitrary
                return True
    return False


def extract_icd10_and_cpt_codes(document: str) -> tuple:
    """Extracts ICD-10 and CPT codes using OpenAI API."""
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "icd_and_cpt_codes",
            "schema": {
                "type": "object",
                "properties": {
                    "icd10Codes": {
                        "description": "The ICD-10 code(s) of the patient's established diagnoses relevant to the prior auth request",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "cptCodes": {
                        "description": "The CPT code(s) of the treatment or procedure the patient is obtaining the prior auth for",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
            },
        },
    }

    prompt = f"""You are an insurance clearinghouse evaluating a prior auth request. 
    Extract the relevant ICD-10 codes for the patient's established diagnoses 
    and CPT codes for the treatment or procedure requiring authorization. 
    Only include codes directly related to the prior auth request. 
    If no relevant codes are found, return empty arrays. 
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "developer",
                "content": f"""${prompt} ${document}""",
            },
        ],
        response_format=response_format,
    )

    response = json.loads(response.choices[0].message.content)
    icd10_codes = response.get("icd10Codes", [])
    cpt_codes = response.get("cptCodes", [])
    return icd10_codes, cpt_codes


def process_document(document: str):
    """Processes a document and prints the extracted codes."""
    chunks = split_into_chunks(document)
    icd10_codes = set()
    cpt_codes = set()

    for chunk in chunks:
        if is_relevant(chunk):
            new_icd10s, new_cpts = extract_icd10_and_cpt_codes(chunk)
            icd10_codes.update(new_icd10s)
            cpt_codes.update(new_cpts)

    print("ICD-10 Codes:", list(icd10_codes))
    print("CPT Codes:", list(cpt_codes))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process clinical text and extract ICD-10 and CPT codes."
    )
    parser.add_argument("input_file", help="Path to the input text file.")
    args = parser.parse_args()

    with open(args.input_file, "r") as file:
        document = file.read()
    process_document(document)
