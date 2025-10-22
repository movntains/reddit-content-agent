from functools import lru_cache

from langchain.agents import create_agent

from . import llm, prompts, schemas, tools


@lru_cache
def get_reddit_agent():
    model = llm.get_gemini_model()
    prompt = prompts.reddit_agent_prompt
    reddit_agent = create_agent(
        model=model,
        tools=tools.reddit_tools,
        system_prompt=prompt,
        response_format=schemas.RedditCommunitiesSchema,
    )

    return reddit_agent


reddit_agent = get_reddit_agent()


def perform_get_reddit_communities(query: str):
    results = reddit_agent.invoke(
        input={"messages": [{"role": "user", "content": f"{query}"}]},
        stream_mode="values",
    )
    community_data = [
        x.model_dump() for x in results["structured_response"].communities
    ]

    return community_data


@lru_cache
def extract_topics_agent(query: str):
    model = llm.get_gemini_model()
    topic_agent = create_agent(
        model=model,
        tools=[],
        system_prompt=prompts.topic_extraction_prompt,
        response_format=schemas.TopicListSchema,
    )

    topic_results = topic_agent.invoke(
        input={"messages": [{"role": "user", "content": f"{query}"}]},
        stream_mode="values",
    )

    return [x.model_dump() for x in topic_results["structured_response"].topics]
