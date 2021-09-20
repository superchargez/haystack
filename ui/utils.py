import os

import requests
import streamlit as st
from haystack import Answer

API_ENDPOINT = os.getenv("API_ENDPOINT", "http://localhost:8000")
DOC_REQUEST = "query"
DOC_FEEDBACK = "feedback"
DOC_UPLOAD = "file-upload"


@st.cache(show_spinner=False)
def retrieve_doc(query, filters=None, top_k_reader=5, top_k_retriever=5):
    # Query Haystack API
    url = f"{API_ENDPOINT}/{DOC_REQUEST}"
    # TODO adjust to new params arg in pipeline
    req = {"query": query, "filters": filters, "top_k_retriever": top_k_retriever, "top_k_reader": top_k_reader}
    response_raw = requests.post(url, json=req).json()

    # Format response
    result = []
    answers: List[Answer] = response_raw["answers"]
    for i in range(len(answers)):
        answer = answers[i]["answer"]
        if answer:
            result.append(
                {
                    "context": "..." + answer.context + "...",
                    "answer": answer,
                    "source": answer.meta["name"],
                    "relevance": round(answer.score * 100, 2),
                    "document_id": answer.document_id,
                    "offset_start_in_doc": answer.offsets_in_document[0].start,
                }
            )
    return result, response_raw


def feedback_doc(question, is_correct_answer, document_id, model_id, is_correct_document, answer, offset_start_in_doc):
    # Feedback Haystack API
    url = f"{API_ENDPOINT}/{DOC_FEEDBACK}"
    #TODO adjust after Label refactoring
    req = {
        "question": question,
        "is_correct_answer": is_correct_answer,
        "document_id": document_id,
        "model_id": model_id,
        "is_correct_document": is_correct_document,
        "answer": answer,
        "offset_start_in_doc": offset_start_in_doc,
    }
    response_raw = requests.post(url, json=req).json()
    return response_raw


def upload_doc(file):
    url = f"{API_ENDPOINT}/{DOC_UPLOAD}"
    files = [("files", file)]
    response_raw = requests.post(url, files=files).json()
    return response_raw
