from langchain.embeddings.base import Embeddings
from langchain.vectorstores.chroma import Chroma
from langchain.schema import BaseRetriever

class RedundantFilterRetriever(BaseRetriever):
    embeddings: Embeddings
    chroma: Chroma
    
    def get_relevant_documents(self, query: str):
        # calculate the embeddings for the query
        query_embedding = self.embeddings.embed_query(query)
        
        # take embedding and feed them into max_marginal_relevance_search_by_vector
        return self.chroma.max_marginal_relevance_search_by_vector(
            query_embedding,
            lambda_mult=0.8
        )
    
    def filter_documents(self):
        return []
