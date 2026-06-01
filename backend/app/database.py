from typing import Optional

from app.models import Todo


class Database:
    def __init__(self):
        self._todos: list[Todo] = []
        self._next_id = 1

    def list_all(self) -> list[Todo]:
        return self._todos

    def get(self, todo_id: int) -> Optional[Todo]:
        return next((t for t in self._todos if t.id == todo_id), None)

    def create(self, data: dict) -> Todo:
        todo = Todo(id=self._next_id, **data)
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def update(self, todo_id: int, data: dict) -> Optional[Todo]:
        todo = self.get(todo_id)
        if todo is None:
            return None
        for key, value in data.items():
            setattr(todo, key, value)
        return todo

    def delete(self, todo_id: int) -> bool:
        todo = self.get(todo_id)
        if todo is None:
            return False
        self._todos.remove(todo)
        return True


db = Database()
