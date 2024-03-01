from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import os
import shutil
import argparse

DATA_PATH = "data"
CHROMA_PATH = "chroma"
OPENAI_API = "secret_key" #I removed it for privacy reasons

PROMPT_TEMPLATE = """

Answer the question based only on the following context:

{context}

---

"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text",type=str,help="The Query Text")
    args = parser.parse_args()
    query_text = args.query_text

    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API)
    db = Chroma(persist_directory=CHROMA_PATH,embedding_function=embedding_function)

    results = db.similarity_search_with_relevance_scores(query_text,k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find closely matching results")

    context_text = "\n\n---\n\n".join([doc.page_content for doc,_score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text,question=query_text)
    print(prompt)

    model = ChatOpenAI(openai_api_key=OPENAI_API)
    response_text = model.predict(prompt)
    sources = [doc.metadata.get("source",None) for doc,_score in results]
    formatted_response = f"Response : {response_text}\n Sources : {sources}"
    print(formatted_response)


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def split_text(documents : list[Document]):
    textsplitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 500,
        length_function = len,
        add_start_index = True
    )   
    chunks = textsplitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks")
    document = chunks[10]
    print(document.page_content)
    print(document.metadata)
    return chunks


def save_to_chroma(chunks:list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(openai_api_key=OPENAI_API),persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}")


def load_documents():
    loader = DirectoryLoader(DATA_PATH,glob="*.txt")
    documents = loader.load()
    return documents


if __name__ == "__main__":
    main()
