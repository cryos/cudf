# Copyright (c) 2018, NVIDIA CORPORATION.

"""
Define how data are formatted
"""
import numbers


def format(index, cols, show_headers=True, more_cols=0, more_rows=0,
           min_width=4, series_spacing=False):
    """
    Format columnar data.

    Parameters
    ----------
    index : Index
    cols : OrderedDict
        A dictionary of `column_name: column_values`, where `column_values` is
        a list of str to be displayed
        It is assumed that all columns has equal length.
    show_headers : bool; defaults to True
        Determines if column headers are showed.
    more_cols : int; defaults to 0
        If `> 0`, a line is added to show the number of remaining cols.
    more_rows : int; defaults to 0
        If `> 0`, a line is added to show the number of remaining rows.
    min_width: int; defaults to 4
        Minimum width of each cell.

    Returns
    -------
    The `str` of the formatted output
    """
    if not cols:
        return "Empty DataFrame\nColumns: {}\nIndex: {}".format(
            list(cols.keys()),
            list(index)
          )

    if len(list(cols.values())[0]) == 0:
        return "Empty DataFrame\nColumns: {}\nIndex: {}".format(
            list(cols.keys()),
            list(index)
        )
    # get number of rows from the first column
    nrows = len(next(iter(cols.values())))
    headers = tuple(cols.keys())
    lastcol = headers[-1] if more_cols > 0 else None

    # offset because Series get more spaces than DFs
    col0_offset = 3 if series_spacing else 1

    # compute column widths
    widths = {}
    for k, vs in cols.items():
        if k == 0 and not series_spacing:
            widths[k] = 1
        elif isinstance(k, numbers.Integral):
            widths[k] = min_width
        else:
            widths[k] = max(len(k)+1, max(map(len, vs), default=0)+col0_offset,
                            min_width)
        for v in vs:
            if len(v) == max(map(len, vs), default=0) and '-' in v and\
                    len(v) > len(k):
                widths[k] = widths[k]-2 if k == 0 else\
                    max(min_width-1, widths[k]-1)
    out = []
    widthkey = min(len(str(nrows)), len(headers[0]))

    cell_template = "{:>{}}"
    #   format headers
    if show_headers and headers[0] != '':
        header = [' ' * widthkey]
        header += [cell_template.format(k, widths[k]) for k in headers[:-1]]
        if lastcol is not None:
            header += ['...']
        header += [cell_template.format(k, widths[k]) for k in headers[-1:]]
        out.append(' '.join(header))
    #   format rows
    if index.name:
        out.append(cell_template.format(str(index.name), 0))
    for i in range(nrows):
        row = [cell_template.format(str(index[i]), 0)]
        for k, vs in cols.items():
            if k == lastcol:
                row.append('...')
            row.append(cell_template.format(vs[i], widths[k]))
        out.append(' '.join(row))

    # show number of remaining rows
    if more_rows > 0:
        out.append("[{} more rows]".format(more_rows))
    # show number of remaining columns
    if more_cols > 0:
        out.append("[{} more columns]".format(more_cols))

    return '\n'.join(out)
