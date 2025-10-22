from functools import lru_cache

from django.conf import settings
from langchain_brightdata import BrightDataSERP


@lru_cache
def get_serp_tool(search_engine: str = "google") -> BrightDataSERP:
    return BrightDataSERP(
        bright_data_api_key=settings.BRIGHT_DATA_API_KEY,
        search_engine=search_engine,
        parse_results=True,
    )


reddit_tools = [get_serp_tool()]
