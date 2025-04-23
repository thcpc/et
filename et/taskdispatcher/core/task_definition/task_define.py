from dataclasses import dataclass
from typing import Optional, Union


@dataclass(frozen=True)
class TaskDefine:
    task_type: Union[int, None]
    document_id: Union[int, None]
    create_user_id: Union[int, None]
    old_assign_user_id: Union[int, None]
    new_assign_user_id: Union[int, None]
    current_task_id: Union[int, None]
    comment: Union[str, None]
