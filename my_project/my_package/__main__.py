{%- if is_cli %}
from .cli import app

app(prog_name="{{my_project}}")
{%- endif %}
