import json
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class ToolDefinition:
    def __init__(self, name, description, input_schema, function):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.function = function

    def __str__(self):
        return self.name


def read_file(input_data):
    input_dict = json.loads(input_data)
    path = input_dict["path"]
    try:
        with open(path, "r") as file:
            content = file.read()
        return content, None
    except Exception as e:
        return "", str(e)


def list_files(input_data):
    input_dict = json.loads(input_data) if input_data else {}
    base_path = input_dict.get("path", ".")
    try:
        results = []
        for root, _, filenames in os.walk(base_path):
            if base_path == ".":
                relative_dir = "."
            else:
                relative_dir = os.path.relpath(root, base_path)
            if relative_dir != ".":
                results.append(f"{relative_dir}/")
            for filename in filenames:
                if relative_dir == ".":
                    results.append(filename)
                else:
                    results.append(os.path.join(relative_dir, filename))
        return json.dumps(results), None
    except Exception as e:
        return "", str(e)


def edit_file(input_data):
    input_dict = json.loads(input_data)
    path = input_dict["path"]
    old_str = input_dict["old_str"]
    new_str = input_dict.get("new_str", "")

    if not path or old_str == new_str:
        return "", "invalid input params"

    file_path = Path(path)
    try:
        if not os.path.exists(file_path) and old_str == "":
            if file_path.parent != Path("."):
                file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(new_str)
            return f"Successfully created file {path}", None
        content = file_path.read_text()
        if old_str not in content and old_str != "":
            return "", "old_str not found in the file"
        new_content = content.replace(old_str, new_str)
        file_path.write_text(new_content)
        return "Successfully edited.", None
    except Exception as e:
        return "", str(e)

def search_chunk():
    pass


class ReadFileInput(BaseModel):
    path: str = Field(
        description="The relative path of a file in the working directory."
    )


class ListFilesInput(BaseModel):
    path: Optional[str] = Field(
        description="Optional relative path to list files from. Defaults to the current directory if not provided.",
        default=None,
    )


class EditFileInput(BaseModel):
    path: str = Field(
        description="The path to the file. If it doesn't exist, the tool creates it automatically."
    )
    old_str: str = Field(
        description="Text to search for - must match exactly and must only have one match exactly."
    )
    new_str: str = Field(description="Text to replace old_str with.")


class SearchChunkInput(BaseModel):
    query: str = Field(description="The search query to find relevant chunks.")
    user_id: Optional[str] = Field(
        description="The user ID of the requester. Optional, but recommended for tracking.",
        default=None,
    )

read_file_definition = ToolDefinition(
    name="read_file",
    description="Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names.",
    input_schema=ReadFileInput.model_json_schema(),
    function=read_file,
)

list_files_definition = ToolDefinition(
    name="list_files",
    description="List files and directories at a given path. If no path is provided, list files in the current directory.",
    input_schema=ListFilesInput.model_json_schema(),
    function=list_files,
)

edit_file_definition = ToolDefinition(
    name="edit_file",
    description="""Make edits to a file.
    Replaces 'old_str' with 'new_str' in the given file. 'old_str' and 'new_str' MUST be different from each other.
    If the file specified with path doesn't exist, it will be created automatically.
    """,
    input_schema=EditFileInput.model_json_schema(),
    function=edit_file,
)

search_chunk_definition = ToolDefinition(
    name="search_chunk",
    description="Search for relevant chunks of text in the document store based on a query of user_id .",
    input_schema=SearchChunkInput.model_json_schema(),
    function=search_chunk,
)
