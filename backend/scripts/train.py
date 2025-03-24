import asyncio
from backend.services.training_service import train_all

if __name__ == "__main__":
    asyncio.run(train_all())