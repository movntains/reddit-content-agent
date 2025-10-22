from pydantic import BaseModel, Field


class RedditCommunitySchema(BaseModel):
    name: str = Field(description="Formatted name for Reddit")
    url: str = Field(description="The complete URL of the Reddit community")
    subreddit_slug: str = Field(
        description="The slug of the subreddit such as r/python, r/web, or r/trending"
    )
    member_count: int | None = Field(description="Current member count, if available")


class RedditCommunitiesSchema(BaseModel):
    communities: list[RedditCommunitySchema] = Field(
        description="The list of Reddit communities"
    )
