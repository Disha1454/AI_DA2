:- use_module(library(csv)).
:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_json)).

% Start the HTTP server
start_server(Port) :-
    http_server(http_dispatch, [port(Port)]).

% Define REST API endpoints
:- http_handler(root(check_eligibility), check_eligibility_handler, []).

% Load attendance data from a CSV file
load_attendance(File) :-
    csv_read_file(File, Rows, [functor(attendance)]),
    maplist(assert, Rows).

% Define rules for scholarship and exam eligibility
eligible_for_scholarship(StudentID) :-
    attendance(StudentID, Percentage),
    Percentage >= 85.

permitted_for_exam(StudentID) :-
    attendance(StudentID, Percentage),
    Percentage >= 75.

% Handle REST API requests for checking eligibility
check_eligibility_handler(Request) :-
    http_read_json(Request, JSONIn),
    _{student_id: StudentID} :< JSONIn,
    check_eligibility(StudentID, Result),
    reply_json(Result).

% Check eligibility and prepare response
check_eligibility(StudentID, Result) :-
    (eligible_for_scholarship(StudentID) ->
        Scholarship = "Eligible for Scholarship";
        Scholarship = "Not Eligible for Scholarship"),
    (permitted_for_exam(StudentID) ->
        Exam = "Permitted for Exam";
        Exam = "Not Permitted for Exam"),
    Result = _{
        student_id: StudentID,
        scholarship_status: Scholarship,
        exam_status: Exam
    }.

% Sample query for testing
% ?- start_server(8080).
% Access the API via POST request at http://localhost:8080/check_eligibility with JSON:
% { "student_id": 101 }
