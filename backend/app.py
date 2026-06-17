from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    try:
        student_data = request.get_json(silent=True) or {}
        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark", 0)

        if not name or not course:
            return jsonify({"error": "name and course are required"}), 404
        if not isinstance(mark, int) or mark < 0 or mark > 100:
            return jsonify({"error": "mark must be an integer between 0 and 100"}), 404

        created_student = db.insert_student(name, course, mark)
        return jsonify(created_student), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    try:
        student_data = request.get_json(silent=True) or {}
        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark")

        if mark is not None and (not isinstance(mark, int) or mark < 0 or mark > 100):
            return jsonify({"error": "mark must be an integer between 0 and 100"}), 404

        updated_student = db.update_student(student_id, name=name, course=course, mark=mark)
        if not updated_student:
            return jsonify({"error": "student not found"}), 404
        return jsonify(updated_student), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    try:
        deleted_student = db.delete_student(student_id)
        if not deleted_student:
            return jsonify({"error": "student not found"}), 404
        return jsonify(deleted_student), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        marks = [student["mark"] for student in students]

        if len(marks) == 0:
            return jsonify({"count": 0, "average": 0, "min": 0, "max": 0}), 200

        stats = {
            "count": len(marks),
            "average": sum(marks) / len(marks),
            "min": min(marks),
            "max": max(marks),
        }
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
