from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, GradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p) :
    """Returns list of assignments submitted to teacher"""

    teacher_assignments = Assignment.get_assignments_submitted_to_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    
    return APIResponse.respond(data=teacher_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):

    submit_assignment_payload = GradeSchema().load(
        {'teacher_id' : p.teacher_id, 
        'id' : incoming_payload['id'], 
        'grade' : incoming_payload['grade']
    })


    assignment = Assignment.make_grade(
        _id = submit_assignment_payload.id, 
        teacher_id = submit_assignment_payload.teacher_id, 
        grade = submit_assignment_payload.grade) 

    teacher_assignments_dump = AssignmentSchema().dump(assignment, many=False)
    
    return APIResponse.respond(data = teacher_assignments_dump)