from pydantic import BaseModel

class CrawlConfigSchema(BaseModel):
    url: str
    depth: int
    use_browser: bool

    model_config = {
        "from_attributes": True
    }