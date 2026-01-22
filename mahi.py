from charan import SessionLocal,Student,Assignment,init_db
from flask import Flask,request,jsonify
app=Flask(__name__)
init_db()
@app.route("/",methods=['GET'])
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
            return jsonify({"message": "student id already present"}), 409
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
        row = s.query(Assignment).filter(Assignment.id == id1).first()
        if row:
            return jsonify({'message':'assignment id already present'}), 409
        st = s.query(Student).filter(Student.id == student1).first()
        if not st:
            return jsonify({'message':'student id not found'}), 404
        water=Assignment(id=id1,topic=topic1,student_id=student1,status=status1)
        s.add(water)
        s.commit()
        out = water.to_dict()
    return jsonify(out),201

@app.route("/panja")
def guru():
    with SessionLocal() as s:
        d=s.query(Assignment).all()
        data=[da.to_dict() for da in d]
    return jsonify(data),201

@app.route("/charan/<int:id>", methods=['PUT','PATCH'])
def up_student(id):
    d = request.get_json(silent=True) or {}
    with SessionLocal() as s:
        r = s.query(Student).filter(Student.id == id).first()
        if not r:
            return jsonify({"message": "student not found"}), 404
        if request.method == 'PUT':
            if d.get('name') is None or d.get('status') is None:
                return jsonify({"message": "name and status are required for PUT"}), 400
        if 'name' in d and d['name'] is not None:
            r.name = d['name']
        if 'status' in d and d['status'] is not None:
            r.status = d['status']
        s.commit()
        return jsonify(r.to_dict()), 200

@app.route("/charan/<int:id>", methods=['DELETE'])
def del_student(id):
    with SessionLocal() as s:
        r = s.query(Student).filter(Student.id == id).first()
        if not r:
            return jsonify({"message": "student not found"}), 404
        s.delete(r)
        s.commit()
        return jsonify({"message": "student deleted"}), 200

@app.route("/assign/<int:id>", methods=['PUT','PATCH'])
def up_assign(id):
    d = request.get_json(silent=True) or {}
    with SessionLocal() as s:
        r = s.query(Assignment).filter(Assignment.id == id).first()
        if not r:
            return jsonify({"message": "assignment not found"}), 404
        if request.method == 'PUT':
            if d.get('topic') is None or d.get('student') is None or d.get('status') is None:
                return jsonify({"message": "topic, student and status are required for PUT"}), 400
        if 'topic' in d and d['topic'] is not None:
            r.topic = d['topic']
        if 'student' in d and d['student'] is not None:
            r.student = d['student']
        if 'status' in d and d['status'] is not None:
            r.status = d['status']
        s.commit()
        return jsonify(r.to_dict()), 200

@app.route("/assign/<int:id>", methods=['DELETE'])
def del_assign(id):
    with SessionLocal() as s:
        r = s.query(Assignment).filter(Assignment.id == id).first()
        if not r:
            return jsonify({"message": "assignment not found"}), 404
        s.delete(r)
        s.commit()
        return jsonify({"message": "assignment deleted"}), 200

if(__name__=='__main__'):
    app.run(debug=True,port=8000)