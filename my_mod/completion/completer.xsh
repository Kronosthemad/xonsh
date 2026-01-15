# ls /tmp/<TAB>
CompletionContext(
    command=CommandContext(
        args=(CommandArg(value='ls'),),
        arg_index=1, prefix='/tmp/',
        ),
    python=PythonContext(multiline_code="ls /tmp/", cursor_index=8, ctx={...})
)

# ls $(whic<TAB> "python") -l
CompletionContext(
    command=CommandContext(
        args=(CommandArg(value='python', opening_quote='"', closing_quote='"'),),
        arg_index=0, prefix='whic', subcmd_opening='$(',
    ),
    python=None
)

# echo @(sys.exe<TAB>)
CompletionContext(
    command=None,
    python=PythonContext(
        multiline_code="sys.exe", cursor_index=7,
        is_sub_expression=True, ctx={...},
    )
)
