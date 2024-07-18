# Imports
import pandas as pd
from langchain_milvus import Milvus, Zilliz
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document



#------------------------- Functions -------------------------------------------

def df_to_documents(df):
    return [Document(page_content=row['chunk'], metadata={'url': row['url']}) for _, row in df.iterrows()]
#-------------------------------------------------------------------------------

if __name__ == '__main__':

    df = pd.read_csv('chunks_merged.csv')

    docs = df_to_documents(df)

    embeddings = HuggingFaceEmbeddings()

    index_params = {
        {'metric_type': 'L2',
        'index_type': 'IVF_FLAT',
        'params': {"nlist": 128}}
    }

    vectorstore = Milvus.from_documents(  # or Zilliz.from_documents
        documents=docs,
        embedding=embeddings,
        collection_name="nvidia",
        connection_args={
            "uri": "./milvus_nvidia.db",
        },
        index_params= index_params,
        drop_old=True,  # Drop the old Milvus collection if it exists
    )

    #vectorstore.add_documents(new_docs)

