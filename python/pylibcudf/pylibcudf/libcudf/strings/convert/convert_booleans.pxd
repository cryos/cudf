# Copyright (c) 2020-2024, NVIDIA CORPORATION.
from libcpp.memory cimport unique_ptr
from pylibcudf.libcudf.column.column cimport column
from pylibcudf.libcudf.column.column_view cimport column_view
from pylibcudf.libcudf.scalar.scalar cimport string_scalar


cdef extern from "cudf/strings/convert/convert_booleans.hpp" namespace \
        "cudf::strings" nogil:
    cdef unique_ptr[column] to_booleans(
        column_view input_col,
        string_scalar true_string) except +

    cdef unique_ptr[column] from_booleans(
        column_view input_col,
        string_scalar true_string,
        string_scalar false_string) except +
