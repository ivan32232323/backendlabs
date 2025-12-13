from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional

from passlib.hash import pbkdf2_sha256


@dataclass
class User:
    id: int
    username: str
    password: str  # hashed


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Record:
    id: int
    user_id: int
    category_id: int
    created_at: str  # ISO 8601
    amount: float


class InMemoryStore:
    def __init__(self) -> None:
        self._user_id = 0
        self._category_id = 0
        self._record_id = 0
        self.users: Dict[int, User] = {}
        self.categories: Dict[int, Category] = {}
        self.records: Dict[int, Record] = {}

    # Users
    def create_user(self, username: str, password_plain: str) -> User:
        if self.get_user_by_username(username) is not None:
            raise ValueError("username_taken")

        self._user_id += 1
        user = User(
            id=self._user_id,
            username=username,
            password=pbkdf2_sha256.hash(password_plain),
        )
        self.users[user.id] = user
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        username_l = username.lower()
        for u in self.users.values():
            if u.username.lower() == username_l:
                return u
        return None

    def verify_password(self, user: User, password_plain: str) -> bool:
        return pbkdf2_sha256.verify(password_plain, user.password)

    def delete_user(self, user_id: int) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            for rid in list(self.records.keys()):
                if self.records[rid].user_id == user_id:
                    del self.records[rid]
            return True
        return False

    def list_users(self) -> List[User]:
        return list(self.users.values())

    # Categories
    def create_category(self, name: str) -> Category:
        self._category_id += 1
        category = Category(id=self._category_id, name=name)
        self.categories[category.id] = category
        return category

    def get_category(self, category_id: int) -> Optional[Category]:
        return self.categories.get(category_id)

    def delete_category(self, category_id: int) -> bool:
        if category_id in self.categories:
            del self.categories[category_id]
            for rid in list(self.records.keys()):
                if self.records[rid].category_id == category_id:
                    del self.records[rid]
            return True
        return False

    def list_categories(self) -> List[Category]:
        return list(self.categories.values())

    # Records
    def create_record(self, user_id: int, category_id: int, amount: float) -> Record:
        self._record_id += 1
        created_at = datetime.now(timezone.utc).isoformat()
        record = Record(
            id=self._record_id,
            user_id=user_id,
            category_id=category_id,
            created_at=created_at,
            amount=amount,
        )
        self.records[record.id] = record
        return record

    def get_record(self, record_id: int) -> Optional[Record]:
        return self.records.get(record_id)

    def delete_record(self, record_id: int) -> bool:
        if record_id in self.records:
            del self.records[record_id]
            return True
        return False

    def filter_records(self, user_id: Optional[int], category_id: Optional[int]) -> List[Record]:
        out: List[Record] = []
        for r in self.records.values():
            if user_id is not None and r.user_id != user_id:
                continue
            if category_id is not None and r.category_id != category_id:
                continue
            out.append(r)
        return out


store = InMemoryStore()


def serialize(obj):
    data = asdict(obj)
    # never expose password hash
    data.pop("password", None)
    return data
