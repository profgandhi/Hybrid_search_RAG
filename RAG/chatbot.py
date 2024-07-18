from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain_milvus import Milvus
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAI
import pandas as pd
from langchain.schema import Document
#------------------------------Functions-----------------------------------------------

def get_milvus_vector_store():
    connection_args = {
        "uri": "./milvus_nvidia.db",
    }
    embeddings = HuggingFaceEmbeddings()
    vectorstore = Milvus(
        collection_name="nvidia",
        embedding=embeddings,
        connection_args=connection_args
    )
    return vectorstore

def get_retriver(vectorstore,docs):

    # Keyword
    bm25_retriever = BM25Retriever.from_documents(docs)
    bm25_retriever.k =  50

    # Milvus Retriver
    retriever_milvus = vectorstore.as_retriever(search_kwargs={"k": 50})


    # Hybrid
    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever_milvus],
                                       weights=[0.3, 1])
    

    # Reranking
    model_reranker = HuggingFaceCrossEncoder(model_name = 'BAAI/bge-reranker-base')
    compressor = CrossEncoderReranker(model = model_reranker, top_n = 10)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=ensemble_retriever,
    )

    return compression_retriever

def df_to_documents(df):
    return [Document(page_content=row['chunk'], metadata={'url': row['url']}) for _, row in df.iterrows()]

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    df = pd.read_csv('chunks_merged.csv')

    docs = df_to_documents(df)


    llm = OpenAI(openai_api_key="YOUR_API_KEY")
    vectorstore = get_milvus_vector_store()

    # Keyword + Semantic + ReRanking
    compression_retriever = get_retriver(vectorstore,docs)


    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=compression_retriever,
    )
    query = 'Why this nvidia?'
    result = qa_chain({"query": query})

    print(result)

