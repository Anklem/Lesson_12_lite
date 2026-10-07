import json


class FileInfo:
    def __init__(self, name: str, path: str, size: int, created_at: float | int, updated_at: float | int):
        self.name = name
        self.path = path
        self.size = size
        self.created_at = created_at
        self.updated_at = updated_at


class FileInfoEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, FileInfo):
            return o.__dict__
        return json.JSONEncoder.default(self, o)


file_info_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "path": {"type": "string"},
            "size": {"type": "number", "minimum": 0},
            "created_at": {"type": "number", "minimum": 0},
            "updated_at": {"type": "number", "minimum": 0}
        }
    },
    "required": ["name", "path", "size", "created_at"]
}