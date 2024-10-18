from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


def session_factory(engine_url):
    engine = create_async_engine(engine_url)
    session = async_sessionmaker(bind=engine)
    return session()
