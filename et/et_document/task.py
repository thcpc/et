from pathlib import Path

from celery import shared_task

from libs.file_handle import FileHandle


@shared_task
def sync_write_data(file_path: str, contents: str):
    FileHandle.write_data(Path(file_path), contents=contents)


@shared_task
def sync_paragraph_data(paragraph_list: list, paragraph: dict, file_path: str):
    content = FileHandle.read_data(Path(file_path))
    paragraph["content"] = content
    paragraph_list.append(paragraph)
    return ""
