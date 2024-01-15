import asyncio
import hashlib
import os
from typing import Final, AsyncGenerator

from sqlalchemy import Column, String, JSON, cast, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI: Final[str] = os.environ.get("DATABASE_URI")

engine = create_async_engine(
    DATABASE_URI,
    future=True,
    echo=True,
)

Base = declarative_base()

# expire_on_commit=False will prevent attributes from being expired
# after commit.
AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)

class RecognisedImage(Base):
    __tablename__ = 'recognised_images'
    image_hash = Column(String, primary_key=True, unique=True)
    telegram_image_link = Column(String)
    recognized_search_terms = Column(JSON)

    def __repr__(self):
       return (
           f"<RecognisedImage("
           f"image_hash={self.image_hash}, "
           f"telegram_image_link={self.telegram_image_link}, "
           f"recognized_search_terms={self.recognized_search_terms})>"
       )

# Initialization block
async def create_tables():
    async with engine.begin() as conn:
        # Use run_sync to run synchronous code in async context
        await conn.run_sync(Base.metadata.create_all)

async def search_image(text: str) -> list:
    async with AsyncSessionFactory() as session:
        # Prepare the query
        stmt = select(
            # RecognisedImage,
            RecognisedImage.telegram_image_link,
        ).filter(
            cast(RecognisedImage.recognized_search_terms, String).contains(text)
        )
        results = await session.execute(stmt)
        recognised_images = results.scalars().all()
        return list(recognised_images)

async def save_image(
        data: bytes,
        text: str,
        link: str,
) -> None:
    # SHA3-512
    hash_object_512 = hashlib.sha3_512()
    hash_object_512.update(data)
    img_hash = hash_object_512.hexdigest()

    new_img = RecognisedImage(
        image_hash=img_hash,
        telegram_image_link=link,
        recognized_search_terms={'service1': text}
    )

    try:
        async with AsyncSessionFactory() as session:
            session.add(new_img)
            await session.commit()
    except:
        print("already exists")

async def main():
    await create_tables()
    await save_image(b'123', 'term1', 'link1')

    print(await search_image('term1'))

if __name__ == '__main__':
    asyncio.run(main())