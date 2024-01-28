from entretien.entretien_core.computing_operation import (
    OperationStream,
    OperationStreamBuilder,
)


def test_no_dependency():
    op_builder = OperationStreamBuilder()
    op_builder.add_value("3").add_addition("3", "7").build()
    op_builder._expected_answers = [3, 10]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_simple_dependency():
    op_builder = OperationStreamBuilder()
    op_builder.add_value("3").add_addition("$0", "4").build()
    op_builder._expected_answers = [3, 7]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_double_dependency():
    op_builder = OperationStreamBuilder()
    op_builder.add_value("20").add_addition("$0", "100").add_addition("$1", "1").build()
    op_builder._expected_answers = [20, 120, 121]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_substraction():
    op_builder = OperationStreamBuilder()
    op_builder.add_value("12").add_subtraction("$0", "3").build()
    op_builder._expected_answers = [12, 9]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_multiplication():
    op_builder = OperationStreamBuilder()
    op_builder.add_value("4").add_multiplication("4", "$0").build()
    op_builder._expected_answers = [4, 16]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_coefficients():
    op_builder = OperationStreamBuilder()
    op_builder.add_value("10").add_value("3").add_multiplication("$0", "$1").add_value(
        "2"
    ).add_value("4").add_multiplication("$3", "$4").add_addition("$2", "$5").build()
    op_builder._expected_answers = [10, 3, 30, 2, 4, 8, 38]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_fibonacci():
    """
    VALUE 0 _
    VALUE 1 _
    ADD $0 $1
    ADD $1 $2
    ADD $2 $3
    ADD $3 $4
    ADD $4 $5
    ADD $5 $6
    ADD $6 $7
    """
    op_builder = OperationStreamBuilder()
    op_builder.add_value("0").add_value("1").add_addition("$0", "$1").add_addition(
        "$1", "$2"
    ).add_addition("$2", "$3").add_addition("$3", "$4").add_addition(
        "$4", "$5"
    ).add_addition(
        "$5", "$6"
    ).add_addition(
        "$6", "$7"
    ).build()
    op_builder._expected_answers = [0, 1, 1, 2, 3, 5, 8, 13, 21]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_backward_dependency():
    """
    2
    ADD $1 20
    VALUE 32 _
    """
    op_builder = OperationStreamBuilder()
    op_builder.add_addition("$1", "20").add_value("32").build()
    op_builder._expected_answers = [52, 32]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_diamond_dependency():
    """
    4
    SUB $1 4
    VALUE 3 _
    ADD 8 $1
    MULT $0 $2
    """
    op_builder = OperationStreamBuilder()
    op_builder.add_subtraction("$1", "4").add_value("3").add_addition(
        "8", "$1"
    ).add_multiplication("$0", "$2").build()
    op_builder._expected_answers = [-1, 3, 11, -11]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_accounting_easy():
    """
    6
    MULT $5 $2
    ADD $5 $0
    VALUE 12 _
    ADD $2 $2
    MULT $3 $2
    SUB $3 $2

    expected_value:
    144
    156
    12
    24
    288
    12
    """
    op_builder = OperationStreamBuilder()
    op_builder.add_multiplication("$5", "$2").add_addition("$5", "$0").add_value(
        "12"
    ).add_addition("$2", "$2").add_multiplication("$3", "$2").add_subtraction(
        "$3", "$2"
    ).build()
    op_builder._expected_answers = [144, 156, 12, 24, 288, 12]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_accounting_medium():
    """
    100
    SUB $47 $9
    SUB 44 $59
    ADD $97 $67
    ADD $1 $1
    SUB $57 $67
    ADD $47 $97
    ADD $59 $59
    SUB $50 $83
    SUB $3 $93
    SUB $4 $74
    SUB $38 $0
    ADD $29 $96
    SUB $46 $97
    SUB $5 $98
    SUB $87 $66
    SUB $86 $25
    SUB $1 $98
    SUB $84 $56
    ADD $38 $78
    ADD $46 $34
    ADD $5 $76
    SUB $3 $93
    ADD $19 $31
    ADD $97 $77
    VALUE $54 _
    SUB $6 $6
    ADD $98 $2
    ADD $59 $67
    SUB $36 $86
    SUB $98 $26
    SUB $16 $7
    VALUE $67 _
    ADD $11 $84
    VALUE $63 _
    ADD $3 $6
    VALUE $44 _
    SUB $68 $5
    ADD $7 $58
    ADD $50 $82
    ADD $88 -936
    ADD $43 $47
    ADD $58 842
    SUB $80 $46
    SUB $33 $96
    SUB $43 $46
    ADD $2 $8
    ADD $59 $9
    VALUE $2 _
    SUB $65 $30
    ADD 135 $65
    ADD $71 $93
    ADD $96 $67
    ADD $6 $38
    SUB $5 $8
    SUB $67 $1
    ADD $4 $71
    VALUE $67 _
    SUB $93 $54
    SUB $51 $3
    ADD 993 -871
    ADD $6 $6
    SUB $71 $65
    ADD $25 $60
    VALUE $59 _
    ADD $6 $51
    SUB $63 $97
    VALUE $67 _
    SUB 3 $59
    ADD $88 $3
    SUB $83 $53
    SUB $50 $49
    ADD $60 865
    VALUE $53 _
    SUB $29 $44
    SUB $96 $25
    ADD $21 $77
    SUB $14 $30
    SUB $27 $50
    ADD $51 $5
    SUB $40 $72
    VALUE $90 _
    ADD $87 $42
    ADD $9 $47
    SUB $97 $1
    ADD $21 $44
    ADD $78 $94
    ADD $21 $71
    ADD -730 $67
    SUB $21 $89
    SUB $83 $25
    ADD $47 $84
    ADD $6 $65
    ADD $32 $22
    ADD $27 $59
    ADD $63 $11
    ADD $65 $60
    ADD $59 $6
    SUB $1 $27
    ADD $27 $83
    SUB $19 $61

    expected_value:
    -119
    -78
    -200
    -156
    285
    -281
    244
    1481
    -281
    -81
    1316
    566
    122
    -281
    -730
    1072
    -78
    -447
    1163
    129
    548
    -281
    10
    -1556
    -41
    0
    -200
    3
    -1225
    200
    -1559
    -119
    0
    122
    88
    -285
    -153
    1884
    1197
    -1214
    -444
    1245
    -807
    -244
    -285
    -481
    41
    -200
    1762
    338
    1478
    247
    1441
    0
    -41
    1638
    -119
    166
    403
    122
    488
    1150
    488
    122
    491
    203
    -119
    -119
    -434
    -3
    1140
    1353
    0
    485
    366
    -1756
    829
    -1475
    -34
    -444
    -766
    -1656
    -281
    -3
    -566
    654
    1072
    -849
    -278
    -3
    -766
    447
    10
    125
    688
    691
    366
    -81
    0
    -1021
    """
    op_builder = OperationStreamBuilder()
    op_builder.add_subtraction("$47", "$9").add_subtraction("44", "$59").add_addition(
        "$97", "$67"
    ).add_addition("$1", "$1").add_subtraction("$57", "$67").add_addition(
        "$47", "$97"
    ).add_addition(
        "$59", "$59"
    ).add_subtraction(
        "$50", "$83"
    ).add_subtraction(
        "$3", "$93"
    ).add_subtraction(
        "$4", "$74"
    ).add_subtraction(
        "$38", "$0"
    ).add_addition(
        "$29", "$96"
    ).add_subtraction(
        "$46", "$97"
    ).add_subtraction(
        "$5", "$98"
    ).add_subtraction(
        "$87", "$66"
    ).add_subtraction(
        "$86", "$25"
    ).add_subtraction(
        "$1", "$98"
    ).add_subtraction(
        "$84", "$56"
    ).add_addition(
        "$38", "$78"
    ).add_addition(
        "$46", "$34"
    ).add_addition(
        "$5", "$76"
    ).add_subtraction(
        "$3", "$93"
    ).add_addition(
        "$19", "$31"
    ).add_addition(
        "$97", "$77"
    ).add_value(
        "$54"
    ).add_subtraction(
        "$6", "$6"
    ).add_addition(
        "$98", "$2"
    ).add_addition(
        "$59", "$67"
    ).add_subtraction(
        "$36", "$86"
    ).add_subtraction(
        "$98", "$26"
    ).add_subtraction(
        "$16", "$7"
    ).add_value(
        "$67"
    ).add_addition(
        "$11", "$84"
    ).add_value(
        "$63"
    ).add_addition(
        "$3", "$6"
    ).add_value(
        "$44"
    ).add_subtraction(
        "$68", "$5"
    ).add_addition(
        "$7", "$58"
    ).add_addition(
        "$50", "$82"
    ).add_addition(
        "$88", "-936"
    ).add_addition(
        "$43", "$47"
    ).add_addition(
        "$58", "842"
    ).add_subtraction(
        "$80", "$46"
    ).add_subtraction(
        "$33", "$96"
    ).add_subtraction(
        "$43", "$46"
    ).add_addition(
        "$2", "$8"
    ).add_addition(
        "$59", "$9"
    ).add_value(
        "$2"
    ).add_subtraction(
        "$65", "$30"
    ).add_addition(
        "135", "$65"
    ).add_addition(
        "$71", "$93"
    ).add_addition(
        "$96", "$67"
    ).add_addition(
        "$6", "$38"
    ).add_subtraction(
        "$5", "$8"
    ).add_subtraction(
        "$67", "$1"
    ).add_addition(
        "$4", "$71"
    ).add_value(
        "$67"
    ).add_subtraction(
        "$93", "$54"
    ).add_subtraction(
        "$51", "$3"
    ).add_addition(
        "993", "-871"
    ).add_addition(
        "$6", "$6"
    ).add_subtraction(
        "$71", "$65"
    ).add_addition(
        "$25", "$60"
    ).add_value(
        "$59"
    ).add_addition(
        "$6", "$51"
    ).add_subtraction(
        "$63", "$97"
    ).add_value(
        "$67"
    ).add_subtraction(
        "3", "$59"
    ).add_addition(
        "$88", "$3"
    ).add_subtraction(
        "$83", "$53"
    ).add_subtraction(
        "$50", "$49"
    ).add_addition(
        "$60", "865"
    ).add_value(
        "$53"
    ).add_subtraction(
        "$29", "$44"
    ).add_subtraction(
        "$96", "$25"
    ).add_addition(
        "$21", "$77"
    ).add_subtraction(
        "$14", "$30"
    ).add_subtraction(
        "$27", "$50"
    ).add_addition(
        "$51", "$5"
    ).add_subtraction(
        "$40", "$72"
    ).add_value(
        "$90"
    ).add_addition(
        "$87", "$42"
    ).add_addition(
        "$9", "$47"
    ).add_subtraction(
        "$97", "$1"
    ).add_addition(
        "$21", "$44"
    ).add_addition(
        "$78", "$94"
    ).add_addition(
        "$21", "$71"
    ).add_addition(
        "-730", "$67"
    ).add_subtraction(
        "$21", "$89"
    ).add_subtraction(
        "$83", "$25"
    ).add_addition(
        "$47", "$84"
    ).add_addition(
        "$6", "$65"
    ).add_addition(
        "$32", "$22"
    ).add_addition(
        "$27", "$59"
    ).add_addition(
        "$63", "$11"
    ).add_addition(
        "$65", "$60"
    ).add_addition(
        "$59", "$6"
    ).add_subtraction(
        "$1", "$27"
    ).add_addition(
        "$27", "$83"
    ).add_subtraction(
        "$19", "$61"
    ).build()
    op_builder._expected_answers = [
        -119,
        -78,
        -200,
        -156,
        285,
        -281,
        244,
        1481,
        -281,
        -81,
        1316,
        566,
        122,
        -281,
        -730,
        1072,
        -78,
        -447,
        1163,
        129,
        548,
        -281,
        10,
        -1556,
        -41,
        0,
        -200,
        3,
        -1225,
        200,
        -1559,
        -119,
        0,
        122,
        88,
        -285,
        -153,
        1884,
        1197,
        -1214,
        -444,
        1245,
        -807,
        -244,
        -285,
        -481,
        41,
        -200,
        1762,
        338,
        1478,
        247,
        1441,
        0,
        -41,
        1638,
        -119,
        166,
        403,
        122,
        488,
        1150,
        488,
        122,
        491,
        203,
        -119,
        -119,
        -434,
        -3,
        1140,
        1353,
        0,
        485,
        366,
        -1756,
        829,
        -1475,
        -34,
        -444,
        -766,
        -1656,
        -281,
        -3,
        -566,
        654,
        1072,
        -849,
        -278,
        -3,
        -766,
        447,
        10,
        125,
        688,
        691,
        366,
        -81,
        0,
        -1021,
    ]

    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_accounting_hard():
    """
    100
    MULT $61 $95
    ADD $26 $80
    ADD $6 $0
    ADD $98 $39
    ADD $72 $14
    SUB $12 $32
    MULT $73 $86
    ADD $80 $12
    MULT $86 $60
    SUB $39 $59
    SUB $64 $83
    SUB $98 $91
    SUB $59 $80
    MULT $65 $73
    ADD $25 $3
    ADD $93 $10
    SUB $93 $72
    MULT $43 $23
    MULT $43 $51
    MULT $71 $0
    SUB $60 $3
    ADD $77 $46
    SUB $23 $40
    MULT $99 $6
    MULT $44 $39
    VALUE $28 _
    VALUE $43 _
    ADD $92 $46
    ADD $49 $86
    SUB $82 $41
    ADD $12 $89
    ADD $91 $86
    SUB $60 $9
    MULT $51 $3
    SUB $12 $94
    ADD $12 $28
    ADD $66 $69
    SUB $53 $1
    ADD $98 $53
    ADD $98 $98
    ADD $42 $59
    SUB $64 $0
    SUB $98 $6
    MULT 609 -14
    ADD $60 $55
    SUB $59 -245
    MULT $64 $1
    MULT $99 $98
    ADD $46 $97
    SUB $86 $43
    MULT $28 $18
    MULT $64 $40
    SUB $70 $32
    MULT $91 $80
    ADD $83 $6
    ADD $97 $76
    MULT $23 $45
    SUB $53 $22
    MULT $6 $10
    ADD $39 $98
    MULT $17 $26
    MULT $93 $59
    SUB $70 $99
    SUB $64 $43
    SUB $9 $9
    MULT $91 $53
    MULT $26 $80
    ADD $9 $43
    SUB $72 $13
    ADD $64 $82
    ADD $80 $45
    SUB $12 $61
    ADD $53 $73
    SUB $43 $98
    MULT $47 $86
    SUB $56 $99
    SUB $53 $51
    ADD 681 $43
    ADD $70 $18
    MULT $12 $51
    MULT $6 $45
    SUB $99 $40
    VALUE $45 _
    SUB $59 $98
    SUB $6 $59
    MULT $55 $51
    SUB $39 $39
    SUB $26 $73
    ADD $84 $92
    ADD $97 $50
    SUB $75 $66
    ADD $86 $43
    MULT 295 $60
    MULT $31 $17
    SUB $9 $11
    SUB $87 $65
    MULT $64 $55
    MULT $49 $23
    MULT -6 380
    VALUE $53 _
    """
    op_builder = OperationStreamBuilder()
    op_builder.add_multiplication("$61", "$95").add_addition("$26", "$80").add_addition(
        "$6", "$0"
    ).add_addition("$98", "$39").add_addition("$72", "$14").add_subtraction(
        "$12", "$32"
    ).add_multiplication(
        "$73", "$86"
    ).add_addition(
        "$80", "$12"
    ).add_multiplication(
        "$86", "$60"
    ).add_subtraction(
        "$39", "$59"
    ).add_subtraction(
        "$64", "$83"
    ).add_subtraction(
        "$98", "$91"
    ).add_subtraction(
        "$59", "$80"
    ).add_multiplication(
        "$65", "$73"
    ).add_addition(
        "$25", "$3"
    ).add_addition(
        "$93", "$10"
    ).add_subtraction(
        "$93", "$72"
    ).add_multiplication(
        "$43", "$23"
    ).add_multiplication(
        "$43", "$51"
    ).add_multiplication(
        "$71", "$0"
    ).add_subtraction(
        "$60", "$3"
    ).add_addition(
        "$77", "$46"
    ).add_subtraction(
        "$23", "$40"
    ).add_multiplication(
        "$99", "$6"
    ).add_multiplication(
        "$44", "$39"
    ).add_value(
        "$28"
    ).add_value(
        "$43"
    ).add_addition(
        "$92", "$46"
    ).add_addition(
        "$49", "$86"
    ).add_subtraction(
        "$82", "$41"
    ).add_addition(
        "$12", "$89"
    ).add_addition(
        "$91", "$86"
    ).add_subtraction(
        "$60", "$9"
    ).add_multiplication(
        "$51", "$3"
    ).add_subtraction(
        "$12", "$94"
    ).add_addition(
        "$12", "$28"
    ).add_addition(
        "$66", "$69"
    ).add_subtraction(
        "$53", "$1"
    ).add_addition(
        "$98", "$53"
    ).add_addition(
        "$98", "$98"
    ).add_addition(
        "$42", "$59"
    ).add_subtraction(
        "$64", "$0"
    ).add_subtraction(
        "$98", "$6"
    ).add_multiplication(
        "609", "-14"
    ).add_addition(
        "$60", "$55"
    ).add_subtraction(
        "$59", "-245"
    ).add_multiplication(
        "$64", "$1"
    ).add_multiplication(
        "$99", "$98"
    ).add_addition(
        "$46", "$97"
    ).add_subtraction(
        "$86", "$43"
    ).add_multiplication(
        "$28", "$18"
    ).add_multiplication(
        "$64", "$40"
    ).add_subtraction(
        "$70", "$32"
    ).add_multiplication(
        "$91", "$80"
    ).add_addition(
        "$83", "$6"
    ).add_addition(
        "$97", "$76"
    ).add_multiplication(
        "$23", "$45"
    ).add_subtraction(
        "$53", "$22"
    ).add_multiplication(
        "$6", "$10"
    ).add_addition(
        "$39", "$98"
    ).add_multiplication(
        "$17", "$26"
    ).add_multiplication(
        "$93", "$59"
    ).add_subtraction(
        "$70", "$99"
    ).add_subtraction(
        "$64", "$43"
    ).add_subtraction(
        "$9", "$9"
    ).add_multiplication(
        "$91", "$53"
    ).add_multiplication(
        "$26", "$80"
    ).add_addition(
        "$9", "$43"
    ).add_subtraction(
        "$72", "$13"
    ).add_addition(
        "$64", "$82"
    ).add_addition(
        "$80", "$45"
    ).add_subtraction(
        "$12", "$61"
    ).add_addition(
        "$53", "$73"
    ).add_subtraction(
        "$43", "$98"
    ).add_multiplication(
        "$47", "$86"
    ).add_subtraction(
        "$56", "$99"
    ).add_subtraction(
        "$53", "$51"
    ).add_addition(
        "681", "$43"
    ).add_addition(
        "$70", "$18"
    ).add_multiplication(
        "$12", "$51"
    ).add_multiplication(
        "$6", "$45"
    ).add_subtraction(
        "$99", "$40"
    ).add_value(
        "$45"
    ).add_subtraction(
        "$59", "$98"
    ).add_subtraction(
        "$6", "$59"
    ).add_multiplication(
        "$55", "$51"
    ).add_subtraction(
        "$39", "$39"
    ).add_subtraction(
        "$26", "$73"
    ).add_addition(
        "$84", "$92"
    ).add_addition(
        "$97", "$50"
    ).add_subtraction(
        "$75", "$66"
    ).add_addition(
        "$86", "$43"
    ).add_multiplication(
        "295", "$60"
    ).add_multiplication(
        "$31", "$17"
    ).add_subtraction(
        "$9", "$11"
    ).add_subtraction(
        "$87", "$65"
    ).add_multiplication(
        "$64", "$55"
    ).add_multiplication(
        "$49", "$23"
    ).add_multiplication(
        "-6", "380"
    ).add_value(
        "$53"
    ).build()
    op_builder._expected_answers = [
        0,
        -8526,
        0,
        -6840,
        -4560,
        -4560,
        0,
        -6840,
        0,
        2280,
        4560,
        6246,
        -6840,
        0,
        1686,
        4560,
        6246,
        0,
        0,
        0,
        6840,
        -7845,
        9120,
        0,
        0,
        8526,
        -8526,
        0,
        8526,
        -6595,
        -6840,
        -8526,
        -2280,
        0,
        -2874,
        1686,
        -6595,
        8526,
        -2280,
        -4560,
        -9120,
        0,
        -2280,
        -8526,
        0,
        -6595,
        0,
        0,
        0,
        8526,
        0,
        0,
        -4315,
        0,
        -4560,
        0,
        0,
        -9120,
        0,
        -6840,
        0,
        0,
        -6595,
        8526,
        0,
        0,
        0,
        -6246,
        -6246,
        -6595,
        -6595,
        -6840,
        -6246,
        -6246,
        0,
        0,
        0,
        -7845,
        -6595,
        0,
        0,
        9120,
        -6595,
        -4560,
        6840,
        0,
        0,
        -2280,
        6840,
        0,
        0,
        -8526,
        0,
        0,
        -3966,
        -2280,
        0,
        0,
        -2280,
        0,
    ]

    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)


def test_birecursion():
    """
    92
    SUB $33 $64
    ADD $60 $60
    ADD $61 $61
    SUB $76 $80
    SUB $25 $59
    ADD $58 $28
    ADD $88 $59
    ADD $32 $32
    ADD $83 $21
    ADD $69 $39
    ADD $57 $64
    ADD $26 $26
    ADD $1 $1
    SUB $62 $68
    ADD $73 $1
    ADD $50 $27
    SUB $24 $2
    ADD $14 $12
    ADD $10 $89
    SUB $67 $35
    ADD $58 $58
    ADD $7 $7
    SUB $0 $89
    ADD $20 $20
    SUB $43 $61
    SUB $53 $11
    ADD $37 $37
    ADD $82 $47
    ADD $90 $2
    ADD $89 $89
    ADD $85 $85
    SUB $91 $47
    ADD $69 $69
    SUB $46 $86
    SUB $42 $20
    ADD $12 $12
    ADD $56 $8
    ADD $72 $72
    ADD $9 $32
    ADD $30 $77
    ADD $80 $48
    ADD $79 $81
    SUB $16 $58
    SUB $44 $56
    SUB $63 $21
    ADD $20 $5
    SUB $49 $81
    ADD $54 $54
    ADD $29 $18
    SUB $34 $23
    ADD $47 $47
    SUB $74 $32
    SUB $17 $72
    SUB $71 $26
    ADD $59 $59
    ADD $15 $68
    ADD $21 $21
    ADD $86 $41
    ADD $2 $2
    ADD $11 $11
    ADD $80 $80
    ADD $56 $56
    SUB $31 $50
    SUB $51 $7
    ADD $86 $86
    ADD $72 $35
    SUB $75 $30
    SUB $70 $12
    ADD $50 $50
    ADD $30 $30
    SUB $84 $1
    SUB $52 $37
    VALUE 1 _
    ADD $40 $60
    SUB $66 $69
    SUB $13 $85
    SUB $22 $29
    ADD $55 $85
    ADD $37 $65
    ADD $23 $45
    ADD $29 $29
    ADD $23 $23
    ADD $54 $6
    ADD $38 $7
    SUB $3 $60
    ADD $68 $68
    ADD $81 $81
    ADD $78 $26
    ADD $87 $11
    ADD $64 $64
    ADD $61 $36
    SUB $4 $54

    expected_answer :
    2130706432
    268435456
    131072
    2013265920
    2147483616
    1074266111
    1073741855
    8192
    1073774591
    1073745919
    1090519039
    8
    536870912
    2147483136
    1610612735
    1073742079
    2147221504
    2147483647
    1107296255
    0
    524288
    16384
    2113929216
    1048576
    2147352576
    2147483632
    4
    1073741951
    1074003967
    33554432
    1024
    2147483520
    4096
    2139095040
    2146435072
    1073741824
    1073807359
    2
    1073750015
    1073743871
    1207959551
    1077936127
    2146959360
    2147418112
    2147450880
    1074790399
    2143289344
    64
    1140850687
    2145386496
    128
    2147475456
    2147483646
    2147483640
    32
    1073742335
    32768
    1082130431
    262144
    16
    134217728
    65536
    2147483392
    2147467264
    8388608
    1073741825
    2147481600
    1073741824
    256
    2048
    1610612736
    2147483644
    1
    1342177279
    2147479552
    2147482624
    2080374784
    1073742847
    1073741827
    1075838975
    67108864
    2097152
    1073741887
    1073758207
    1879048192
    512
    4194304
    1073741831
    1073741839
    16777216
    1073872895
    2147483584
    """
    op_builder = OperationStreamBuilder()
    op_builder.add_subtraction("$33", "$64").add_addition("$60", "$60").add_addition(
        "$61", "$61"
    ).add_subtraction("$76", "$80").add_subtraction("$25", "$59").add_addition(
        "$58", "$28"
    ).add_addition(
        "$88", "$59"
    ).add_addition(
        "$32", "$32"
    ).add_addition(
        "$83", "$21"
    ).add_addition(
        "$69", "$39"
    ).add_addition(
        "$57", "$64"
    ).add_addition(
        "$26", "$26"
    ).add_addition(
        "$1", "$1"
    ).add_subtraction(
        "$62", "$68"
    ).add_addition(
        "$73", "$1"
    ).add_addition(
        "$50", "$27"
    ).add_subtraction(
        "$24", "$2"
    ).add_addition(
        "$14", "$12"
    ).add_addition(
        "$10", "$89"
    ).add_subtraction(
        "$67", "$35"
    ).add_addition(
        "$58", "$58"
    ).add_addition(
        "$7", "$7"
    ).add_subtraction(
        "$0", "$89"
    ).add_addition(
        "$20", "$20"
    ).add_subtraction(
        "$43", "$61"
    ).add_subtraction(
        "$53", "$11"
    ).add_addition(
        "$37", "$37"
    ).add_addition(
        "$82", "$47"
    ).add_addition(
        "$90", "$2"
    ).add_addition(
        "$89", "$89"
    ).add_addition(
        "$85", "$85"
    ).add_subtraction(
        "$91", "$47"
    ).add_addition(
        "$69", "$69"
    ).add_subtraction(
        "$46", "$86"
    ).add_subtraction(
        "$42", "$20"
    ).add_addition(
        "$12", "$12"
    ).add_addition(
        "$56", "$8"
    ).add_addition(
        "$72", "$72"
    ).add_addition(
        "$9", "$32"
    ).add_addition(
        "$30", "$77"
    ).add_addition(
        "$80", "$48"
    ).add_addition(
        "$79", "$81"
    ).add_subtraction(
        "$16", "$58"
    ).add_subtraction(
        "$44", "$56"
    ).add_subtraction(
        "$63", "$21"
    ).add_addition(
        "$20", "$5"
    ).add_subtraction(
        "$49", "$81"
    ).add_addition(
        "$54", "$54"
    ).add_addition(
        "$29", "$18"
    ).add_subtraction(
        "$34", "$23"
    ).add_addition(
        "$47", "$47"
    ).add_subtraction(
        "$74", "$32"
    ).add_subtraction(
        "$17", "$72"
    ).add_subtraction(
        "$71", "$26"
    ).add_addition(
        "$59", "$59"
    ).add_addition(
        "$15", "$68"
    ).add_addition(
        "$21", "$21"
    ).add_addition(
        "$86", "$41"
    ).add_addition(
        "$2", "$2"
    ).add_addition(
        "$11", "$11"
    ).add_addition(
        "$80", "$80"
    ).add_addition(
        "$56", "$56"
    ).add_subtraction(
        "$31", "$50"
    ).add_subtraction(
        "$51", "$7"
    ).add_addition(
        "$86", "$86"
    ).add_addition(
        "$72", "$35"
    ).add_subtraction(
        "$75", "$30"
    ).add_subtraction(
        "$70", "$12"
    ).add_addition(
        "$50", "$50"
    ).add_addition(
        "$30", "$30"
    ).add_subtraction(
        "$84", "$1"
    ).add_subtraction(
        "$52", "$37"
    ).add_value(
        "1"
    ).add_addition(
        "$40", "$60"
    ).add_subtraction(
        "$66", "$69"
    ).add_subtraction(
        "$13", "$85"
    ).add_subtraction(
        "$22", "$29"
    ).add_addition(
        "$55", "$85"
    ).add_addition(
        "$37", "$65"
    ).add_addition(
        "$23", "$45"
    ).add_addition(
        "$29", "$29"
    ).add_addition(
        "$23", "$23"
    ).add_addition(
        "$54", "$6"
    ).add_addition(
        "$38", "$7"
    ).add_subtraction(
        "$3", "$60"
    ).add_addition(
        "$68", "$68"
    ).add_addition(
        "$81", "$81"
    ).add_addition(
        "$78", "$26"
    ).add_addition(
        "$87", "$11"
    ).add_addition(
        "$64", "$64"
    ).add_addition(
        "$61", "$36"
    ).add_subtraction(
        "$4", "$54"
    ).build()
    op_builder._expected_answers = [
        2130706432,
        268435456,
        131072,
        2013265920,
        2147483616,
        1074266111,
        1073741855,
        8192,
        1073774591,
        1073745919,
        1090519039,
        8,
        536870912,
        2147483136,
        1610612735,
        1073742079,
        2147221504,
        2147483647,
        1107296255,
        0,
        524288,
        16384,
        2113929216,
        1048576,
        2147352576,
        2147483632,
        4,
        1073741951,
        1074003967,
        33554432,
        1024,
        2147483520,
        4096,
        2139095040,
        2146435072,
        1073741824,
        1073807359,
        2,
        1073750015,
        1073743871,
        1207959551,
        1077936127,
        2146959360,
        2147418112,
        2147450880,
        1074790399,
        2143289344,
        64,
        1140850687,
        2145386496,
        128,
        2147475456,
        2147483646,
        2147483640,
        32,
        1073742335,
        32768,
        1082130431,
        262144,
        16,
        134217728,
        65536,
        2147483392,
        2147467264,
        8388608,
        1073741825,
        2147481600,
        1073741824,
        256,
        2048,
        1610612736,
        2147483644,
        1,
        1342177279,
        2147479552,
        2147482624,
        2080374784,
        1073742847,
        1073741827,
        1075838975,
        67108864,
        2097152,
        1073741887,
        1073758207,
        1879048192,
        512,
        4194304,
        1073741831,
        1073741839,
        16777216,
        1073872895,
        2147483584,
    ]
    from entretien.code.computing_operation import main

    with op_builder as stream:
        main(stream)
