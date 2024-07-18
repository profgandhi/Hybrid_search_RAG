### Advanced RAG Features

- Milvus;
- Keyword + Semantic + ReRanking Search
- FLAT_IVF
- Semmantic Segmentation of text
- Custom 5 Hop crawler to get content from root link

#### Order of files

 - get_five_hop_links.py
 - ingest_data.py
 - Semantic_Chunking.py
 - vector_db_milvus.py
 - chatbot.py


#### 1> get_five_hop_links.py
The code is a **web crawler** that explores and extracts URLs from a given webpage up to a specified depth. It uses BeautifulSoup for HTML parsing and requests for HTTP requests. Internal and external URLs are classified and stored in separate sets during the crawling process. The main function, **get_n_hop_links**, manages the crawling depth and processes URLs accordingly. Finally, the collected internal links are **saved into a CSV** file using pandas. This code effectively allows for deep web scraping starting from a specified URL.

#### 2> ingest_data.py
The code is an **asynchronous web scraper** designed to fetch and **parse HTML** content from a list of URLs. It uses aiohttp for asynchronous HTTP requests and html2text to convert HTML content into plain text. The **URLs are read from a CSV** file and **processed in chunks of 5000 to manage large datasets efficiently**. The fetched HTML content is stored in separate CSV files, and then the content is parsed and saved into new CSV files. This approach ensures efficient and **scalable web scraping** with asynchronous processing.

#### 3> Semantic_Chunking.py
The  code processes parsed documents by **cleaning** the data, **generating embeddings**, and splitting the text into **semantic chunks**. It first removes duplicates and short texts from the data, then initializes an embedding model from HuggingFace. The cleaned documents are converted into a specific format and processed using a **semantic splitter,** which groups sentences based on **embedding similarities**. The resulting chunks are saved into CSV files, facilitating efficient text analysis and retrieval.
#### 4> vector_db_milvus.py
The code initializes a **Milvus vector store** for efficient similarity search and retrieval of document chunks. It reads processed text chunks from a CSV file, converts them into a document format, and generates **embeddings using a HuggingFace model**. The documents and their embeddings are then indexed in a Milvus collection with parameters specifying an **L2 distance** metric, an **IVF_FLAT** index type, and **128 clusters** for efficient vector search. The Milvus collection is created anew by dropping any existing collection with the same name. This setup facilitates **fast and accurate retrieval** of similar text chunks from a large dataset.

#### 5> chatbot.py
The  code sets up an **advanced document retrieval** and question-answering system using a combination of **keyword and semantic search** techniques. It reads processed document chunks from a CSV file and initializes a Milvus vector store with HuggingFace embeddings. The retrieval system employs a **BM25 retriever** for keyword search and a Milvus retriever for semantic search, combined using an **ensemble retriever**. A HuggingFace **cross-encoder reranker** is then used to refine the top results. The final retrieval and QA system leverages OpenAI's language model to answer queries based on the retrieved and reranked documents.

###End
