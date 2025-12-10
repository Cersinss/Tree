from bst import BinarySearchTree


def main() -> None:
    tree = BinarySearchTree[int, str]()

    print("=== insert ===")
    for key, value in [(5, "root"), (2, "left"), (8, "right"), (1, "min"), (3, "mid")]:
        tree.insert(key, value)
    print(f"size={len(tree)}, height={tree.height()}, balanced={tree.is_balanced()}")

    print("\n=== search ===")
    for key in [3, 7]:
        print(f"key={key} -> {tree.search(key)}")

    print("\n=== delete ===")
    for key in [2, 5]:
        print(f"delete {key}: {tree.delete(key)}")
    print(f"size={len(tree)}, height={tree.height()}, balanced={tree.is_balanced()}")


if __name__ == "__main__":
    main()

