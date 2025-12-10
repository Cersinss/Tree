from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class TreeNode(Generic[K, V]):
    key: K
    value: V
    left: Optional["TreeNode[K, V]"] = None
    right: Optional["TreeNode[K, V]"] = None
    parent: Optional["TreeNode[K, V]"] = None

    def __repr__(self) -> str:
        return f"TreeNode(key={self.key!r}, value={self.value!r})"


class BinarySearchTree(Generic[K, V]):

    def __init__(self) -> None:
        self.root: Optional[TreeNode[K, V]] = None
        self._size = 0

    def insert(self, key: K, value: V) -> TreeNode[K, V]:
        if self.root is None:
            self.root = TreeNode(key, value)
            self._size = 1
            return self.root

        current = self.root
        while True:
            if key == current.key:
                current.value = value
                return current
            if key < current.key:
                if current.left is None:
                    current.left = TreeNode(key, value, parent=current)
                    self._size += 1
                    return current.left
                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(key, value, parent=current)
                    self._size += 1
                    return current.right
                current = current.right

    def search(self, key: K) -> Optional[V]:
        node = self._find_node(key)
        return node.value if node else None

    def delete(self, key: K) -> bool:
        node = self._find_node(key)
        if node is None:
            return False

        self._delete_node(node)
        self._size -= 1
        return True

    def height(self) -> int:
        return self._height(self.root)

    def is_balanced(self) -> bool:
        return self._is_balanced(self.root)[0]

    def __len__(self) -> int:
        return self._size

    def _find_node(self, key: K) -> Optional[TreeNode[K, V]]:
        current = self.root
        while current:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return None

    def _transplant(self, u: TreeNode[K, V], v: Optional[TreeNode[K, V]]) -> None:
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _delete_node(self, node: TreeNode[K, V]) -> None:
        if node.left is None:
            self._transplant(node, node.right)
        elif node.right is None:
            self._transplant(node, node.left)
        else:
            successor = self._minimum(node.right)
            if successor.parent != node:
                self._transplant(successor, successor.right)
                successor.right = node.right
                if successor.right:
                    successor.right.parent = successor
            self._transplant(node, successor)
            successor.left = node.left
            if successor.left:
                successor.left.parent = successor

    def _minimum(self, node: TreeNode[K, V]) -> TreeNode[K, V]:
        while node.left:
            node = node.left
        return node

    def _height(self, node: Optional[TreeNode[K, V]]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def _is_balanced(self, node: Optional[TreeNode[K, V]]) -> Tuple[bool, int]:
        if node is None:
            return True, 0

        left_balanced, left_height = self._is_balanced(node.left)
        right_balanced, right_height = self._is_balanced(node.right)

        balanced = (
            left_balanced
            and right_balanced
            and abs(left_height - right_height) <= 1
        )
        return balanced, 1 + max(left_height, right_height)

