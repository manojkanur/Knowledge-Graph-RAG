"""Traditional RAG Pipeline using LangChain, OpenAI, and FAISS."""

import os
import time
from typing import List, Dict, Any
from pathlib import Path

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate


class TraditionalRAG:
    """Traditional RAG system using vector similarity search."""

    def __init__(
        self,
        openai_api_key: str,
        model_name: str = "gpt-4-turbo-preview",
        embedding_model: str = "text-embedding-3-small",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize Traditional RAG system.

        Args:
            openai_api_key: OpenAI API key
            model_name: LLM model to use
            embedding_model: Embedding model to use
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize components
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_key=openai_api_key
        )

        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            openai_api_key=openai_api_key
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

        self.vectorstore = None
        self.qa_chain = None

    def load_documents(self, file_path: str) -> List[Document]:
        """
        Load documents from file.

        Args:
            file_path: Path to the document file

        Returns:
            List of LangChain Documents
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split into chunks
        chunks = self.text_splitter.split_text(content)

        # Create Document objects
        documents = [
            Document(page_content=chunk, metadata={"source": file_path, "chunk_id": i})
            for i, chunk in enumerate(chunks)
        ]

        print(f"Loaded {len(documents)} chunks from {file_path}")
        return documents

    def build_index(self, documents: List[Document]) -> None:
        """
        Build FAISS vector index from documents.

        Args:
            documents: List of LangChain Documents
        """
        print("Building FAISS index...")
        start_time = time.time()

        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )

        build_time = time.time() - start_time
        print(f"FAISS index built in {build_time:.2f} seconds")

        # Create QA chain
        self._create_qa_chain()

    def _create_qa_chain(self) -> None:
        """Create the QA chain with custom prompt."""
        prompt_template = """You are a helpful AI assistant answering questions about the CloudStore API documentation.

Use the following pieces of context to answer the question at the end. If you don't know the answer based on the context, say so - don't make up information.

Context:
{context}

Question: {question}

Answer: """

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG system.

        Args:
            question: User's question

        Returns:
            Dictionary with answer, source documents, and metrics
        """
        if not self.qa_chain:
            raise ValueError("Index not built. Call build_index() first.")

        print(f"\nQuerying Traditional RAG: {question}")
        start_time = time.time()

        # Execute query
        result = self.qa_chain.invoke({"query": question})

        query_time = time.time() - start_time

        # Extract results
        answer = result['result']
        source_docs = result['source_documents']

        # Calculate metrics
        num_tokens = len(answer.split())  # Rough estimate
        num_chunks = len(source_docs)

        return {
            "answer": answer,
            "source_documents": source_docs,
            "metrics": {
                "query_time": query_time,
                "num_source_chunks": num_chunks,
                "answer_tokens": num_tokens,
                "retrieval_method": "vector_similarity"
            }
        }

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search without generation.

        Args:
            query: Search query
            k: Number of results

        Returns:
            List of similar documents
        """
        if not self.vectorstore:
            raise ValueError("Index not built. Call build_index() first.")

        return self.vectorstore.similarity_search(query, k=k)

    def save_index(self, path: str) -> None:
        """Save FAISS index to disk."""
        if self.vectorstore:
            self.vectorstore.save_local(path)
            print(f"Index saved to {path}")

    def load_index(self, path: str) -> None:
        """Load FAISS index from disk."""
        self.vectorstore = FAISS.load_local(
            path,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )
        self._create_qa_chain()
        print(f"Index loaded from {path}")
