from sqlalchemy import Column, Integer, String, DateTime, Interval
from sqlalchemy.orm import DeclarativeBase, class_mapper


class Base(DeclarativeBase):
    ...


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, nullable=False)
    task_oid = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    create_time = Column(DateTime, nullable=False)
    start_time = Column(DateTime)
    exec_time = Column(Interval)

    def to_dict(self):
        return {c.key: getattr(self, c.key)
                for c in class_mapper(self.__class__).columns}
