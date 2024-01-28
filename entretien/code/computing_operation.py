from entretien.entretien_core.computing_operation import (
    OperationLine,
    OperationStream,
    OperationType,
)

"""
the stream operation stream is an iterable of operations to execute
it contains the number of line inside the stream and can be iterated
to get the operations to execute.
The possible operation are enumerated in OperationType.
The operation can be VALUE, ADD, MULTIPLE, SUBSTRACT.
Each argument of the operation is a string, and can take 3 types of values:
- a number (ex: "1")
- a reference to a previous operation result (ex: "$1")
- nothing (ex: "_")
The result of each operation must be given in the order the operations were read.
This can be done by calling the add_line_answer method of the stream.

Example:
The solution for ["VALUE 1 _", "VALUE 3 _", "ADD 1 1"] is [1, 3, 2]
The solution for ["VALUE 1 _", "VALUE 3 _", "ADD $1 0"] is [1, 3, 1]
The solution for ["VALUE 1 _", "VALUE 3 _", "ADD $2 0"] is [1, 3, 3]

"""

def main(stream: OperationStream) -> None:
    nb_line = stream.number_of_operations
    for stream_line in stream:
        if stream_line.operation_type == OperationType.VALUE:
            stream.add_line_answer(int(stream_line.arg_1))
        if stream_line.operation_type == OperationType.ADD:
            stream.add_line_answer(int(stream_line.arg_1) + int(stream_line.arg_2))
