

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os
import time

''' load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
if not DATABASE_URL:
    raise RuntimeError("Missing DB_URL in environment (.env).")

# Engine: pre_ping to avoid stale connections; Cockroach serverless typically needs sslmode=require
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()
'''
DATABASE_URL = "sqlite:///charan.db"
 
# Engine + Session factory
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)

    assignments = relationship(
        "Assignment",
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name, "status": self.status}


class Assignment(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String, nullable=False)  # changed to String
    status = Column(String, nullable=False)
    student_id = Column(
        Integer,
        ForeignKey("student.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    student = relationship("Student", back_populates="assignments")

    def to_dict(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "student": self.student_id,
            "status": self.status,
        }


def init_db():
    Base.metadata.create_all(engine)





if __name__ == "__main__":
    init_db()
    print("Tables created and sample data inserted.")

