{%- if is_cli %}
from .cli import app

app(prog_name="{{project_name}}")
{%- endif %}
