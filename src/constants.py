# TODO: maybe do unary operation ~
EXPRESSION_TOKEN = r"""
\s*
(
    \d+(?:\.\d+)?
    | \*\*
    | //
    | [%()+\-*/]
)
"""
