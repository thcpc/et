from et_document.task.core.task_definition.assign_auto_task_generator import AssignAutoTaskGenerator
from et_document.task.core.task_definition.execute_auto_task_generator import ExecuteAutoTaskGenerator
from et_document.task.core.task_definition.execute_regression_task_generator import ExecuteRegressionTaskGenerator
from et_document.task.core.task_definition.link_auto_task_generator import LinkAutoTaskGenerator
from et import enums


def TaskGeneratorFactory(session, task_define):
    return TaskGeneratorClass(task_define.task_type)(session, task_define)


def TaskGeneratorClass(task_type: int):
    return {enums.Name.TaskType.AssignAutoTaskGenerator: AssignAutoTaskGenerator,
            enums.Name.TaskType.ExecuteAutoTaskGenerator: ExecuteAutoTaskGenerator,
            enums.Name.TaskType.LinkAutoTaskGenerator: LinkAutoTaskGenerator,
            enums.Name.TaskType.ExecuteRegressionTaskGenerator: ExecuteRegressionTaskGenerator,
            }.get(int(task_type))