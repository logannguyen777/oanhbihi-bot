from pydantic import BaseModel

class CrawlConfigSchema(BaseModel):
    url: str
    depth: int
    use_browser: bool

    class Config:
        orm_mode = True
