from sqlalchemy.orm import Session
from models import CrawlConfig

def get_crawl_config(db: Session):
    return db.query(CrawlConfig).first()

def update_crawl_config(db: Session, data: dict):
    config = db.query(CrawlConfig).first()
    if config:
        for k, v in data.items():
            setattr(config, k, v)
    else:
        config = CrawlConfig(**data)
        db.add(config)
    db.commit()
    return config