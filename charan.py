from sqlalchemy import create_engine, Column, Integer, String,relationship,ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
 
# Same SQLite file; switch to another DB by changing the URL
DATABASE_URL = "sqlite:///charan.db"
 
# Engine + Session factory
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
 
Base=declarative_base()
class Student(Base):
    __tablename__='student'
    id=Column(Integer ,primary_key=True)
    name=Column(String,nullable=False)
    status=Column(String,nullable=False)
    
    assignments = relationship(
        "Assignment",
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True
     )

    def to_dict(self):
        return {"id":self.id,"name":self.name,"status":self.status}
class Assigment(Base):
    __tablename__='progress'
    id=Column(Integer ,primary_key=True)
    topic=Column(Integer,nullable=False)
    
    status=Column(String,nullable=False)
    
    student_id = Column(
        Integer,
        ForeignKey("student.id", ondelete="CASCADE"),
        nullable=False
    )

    student = relationship("Student", back_populates="assignments")

    def to_dict(self):
        return {"id":self.id,"topic":self.topic,"student":self.student,"status":self.status}
def init_db():
    Base.metadata.create_all(engine)
    
