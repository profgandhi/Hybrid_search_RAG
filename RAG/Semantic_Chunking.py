# Imports
import pandas as pd
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.schema import Document
from llama_index.core.node_parser import SemanticSplitterNodeParser


#---------------------------------------Functions-------------------------------------------------

def clean_df(df):
    df = df.drop_duplicates(subset=['parsed_docs'])
    df = df[~(df['parsed_docs'].str.contains('utf-8'))]
    df['num_words'] = df['parsed_docs'].str.split().apply(lambda x: len(x))
    df = df[df['num_words'] > 30]
    return df

def get_embed_model():
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5",embed_batch_size=100)
    return embed_model

def df_to_documents(df):
    return [Document(text=row['parsed_docs'], metadata={'url': row['links']}) for _, row in df.iterrows()]


#---------------------------------------------------------------------------------------------------



if __name__ == '__main__':

    embed_model = get_embed_model()

    for i in range(0,6):

        df = pd.read_csv(f'parsed_docs{i}.csv')
        df =  clean_df(df)
        docs = df_to_documents(df)

        splitter = SemanticSplitterNodeParser(
            buffer_size=5,  # Group 5 sentences
            breakpoint_percentile_threshold=95, # 95 threshold
            embed_model=embed_model #Embed Model
        )

        nodes = splitter.get_nodes_from_documents(docs,show_progress=True)

        chunks = pd.DataFrame([{'chunk': i.text, 'url': i.metadata['url']} for i in nodes])

        chunks.to_csv(f'chunks{i}.csv')

        del df