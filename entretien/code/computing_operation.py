from entretien.entretien_core.computing_operation import (
    OperationLine,
    OperationStream,
    OperationType,
)


def main(stream: OperationStream) -> None:
    nb_line = stream.number_of_operations
    for stream_line in stream:
        if stream_line.operation_type == OperationType.VALUE:
            stream.add_line_answer(int(stream_line.arg_1))
        if stream_line.operation_type == OperationType.ADD:
            stream.add_line_answer(int(stream_line.arg_1) + int(stream_line.arg_2))
