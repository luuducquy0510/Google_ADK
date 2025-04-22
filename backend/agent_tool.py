from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools import DuckDuckGoSearchResults
from utils import embedding_model
from app_config import settings



def web_search_tool(topic: str):
    """Perform an online web search to retrieve the latest information about the given topic."""
    search = DuckDuckGoSearchResults(
        output_format="list",
        max_results=50
        )
    a = search.invoke(f"""{topic}""")
    return a

def rag_tool(query: str):
    """
    Perform a search in the Milvus database to retrieve relevant documents based on the given query.
    The search is performed using the embedding model to find similar documents.
    """
    docs: list[str] = []

    # print(embedding.embedder.embed_query(query))
    results = settings.MILVUS_CLIENT.search(
        collection_name = "pdf_documents",
        data = [embedding_model.embed_query(query)],
        output_fields=["text"],
        filter = "",
        limit = 4,
    )
    print(results[0])
    for res in results[0]:
        docs.append(res["entity"]["text"])
    
    return docs
