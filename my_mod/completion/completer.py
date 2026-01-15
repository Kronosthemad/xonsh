# Helper decorators for completers:
from xonsh.completers.tools import *

@contextual_command_completer_for('..')
def dummy_completer():
    return {"cd .."}


@contextual_completer
def python_context_completer(context):
    if context.python:
        last_name = context.python.prefix.split()[-1]
        return {i for i in context.python.ctx if i.startswith(last_name)}
    return None


@contextual_completer
def case_completer(context):
    if (not context.command or not (context.command.arg_index == 1) or not (
            context.command.args[0].value == 'cd') or not '*'.startswith(context.command.prefix)):
        return None
    entry = os.DirEntry()
    if entry.__dir__().__str__().lower != dir().__str__().lower:
        return None
    else:
        return dict()


# Save boilerplate with this helper decorator:

@contextual_command_completer_for("cd..")
def better_unbeliever_completer(command):
    """Like unbeliever_completer but with less boilerplate"""
    if command.arg_index == 1 and '\n'.startswith(command.prefix):
        return {'cd ..'}, len('cd..') + len(command.prefix)
    return None


@contextual_command_completer
def remove_quotes(command):
    """
    Return a completer that will remove the quotes, i.e:
    which "python"<TAB> -> which python
    echo "hi<TAB> -> echo hi
    ls "file with spaces"<TAB> -> ls file with spaces
    """
    raw_prefix_len = len(command.raw_prefix)  # this includes the closing quote if it exists
    return {RichCompletion(command.prefix, prefix_len=raw_prefix_len, append_closing_quote=False)}
