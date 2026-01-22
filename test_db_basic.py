
import pytest
from charan import SessionLocal, init_db, Student, Assigment

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()   # DB + tables create
    yield

def test_student_table_insert_and_read():
    s = SessionLocal()
    obj = Student(id=1, name="test", status="ok")
    s.add(obj)
    s.commit()

    rows = s.query(Student).all()
    assert len(rows) >= 1
    s.close()


def test_assignment_table_insert_and_read():
    s = SessionLocal()

    st = Student(id=2, name="ram", status="active")
    s.add(st)
    s.commit()

    a = Assigment(id=10, topic="NLP", status="done", student_id=2)
    s.add(a)
    s.commit()

    rows = s.query(Assigment).all()
    assert len(rows) >= 1
    s.close()
