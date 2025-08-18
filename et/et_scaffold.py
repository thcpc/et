import os
from pathlib import Path

import click


@click.command()
@click.option("--app", prompt="app name", help="app directory name", type=click.Path(exists=True))
@click.option("--name", prompt="module name", help="module directory name")
def create_module(app, name):
    _module_path = Path(app).joinpath(name)
    os.makedirs(_module_path)
    with open(_module_path.joinpath("__init__.py"), 'w') as f:
        f.write("")

    with open(_module_path.joinpath("relationship_def.py"), 'w') as f:
        f.write("#定义该模块下数据关系\n")
        f.write("from sqlalchemy.orm import relationship\n")
        f.write("import et.models as MetaModel\n")

    with open(_module_path.joinpath("service.py"), 'w') as f:
        f.write("#定义该模块的功能函数\n")
        f.write("")

    with open(_module_path.joinpath("view_api.py"), 'w') as f:
        f.write("#定义客户端的调用API\n")
        f.write(f"from {app}.{name} import service as {name}_service\n")

    with open(_module_path.joinpath("facade_api.py"), 'w') as f:
        f.write("#其它模块需要本模块数据聚合调用的API\n")
        f.write(f"from {app}.{name} import service as {name}_service\n")

    with open(Path(app).joinpath("views.py"), 'a') as f:
        f.write(f"import {app}.{name}.view_api as {name}_view_api\n")
    click.secho(f"Created Module: {name} Success", fg="green", bold=True)



if __name__ == "__main__":
    create_module()