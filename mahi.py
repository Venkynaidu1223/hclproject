from charan import SessionLocal,Student,Assigment,init_db
from flask import Flask,request,jsonify
app=Flask(__name__)
init_db()
@app.route("/")
def indu():
    with SessionLocal() as s:
        rows=s.query(Student).all()
        data = [r.to_dict() for r in rows]
        return jsonify(data), 200

@app.route("/charan",methods=['POST'])
def sam():
    d=request.get_json(silent=True) or {}
    id1=d.get('id')
    name1=d.get('name')
    status1=d.get('status')
    if id1 is None or name1 is None or status1 is None:
        return "some values are missing please check"
    with SessionLocal() as s:
        exists = s.query(Student).filter(Student.id == id1).first()
        if exists:
            return jsonify({"message": "already exists, no need"}), 409
        d=Student(id=id1,name=name1,status=status1)
        s.add(d)
        s.commit()
        d=d.to_dict()
    return jsonify(d),201
@app.route("/assign",methods=['POST'])
def fam():
    d=request.get_json(silent=True) or {}
    id1=d.get('id')
    topic1=d.get('topic')
    student1=d.get('student')
    status1=d.get('status')
    if id1 is None or topic1 is None or student1 is None or status1 is None:
        return jsonify({'meassage':'ur missing some values'})
    with SessionLocal() as s:
        rows=s.query(Assigment).filter(id==id1).first()
        if rows:
            return jsonify({'message':'already present'})
        water=Assigment(id=id1,topic=topic1,student=student1,status=status1)
        s.add(water)
        s.commit()
    return jsonify(d),201
@app.route("/panja")
def guru():
    with SessionLocal() as s:
        d=s.query(Assigment).all()
        data=[da.to_dict() for da in d]
    return jsonify(data),201
if(__name__=='__main__'):
    app.run(debug=True,port=8000)