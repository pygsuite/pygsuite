from typing import Any, Optional, Iterable, Callable


class WatchedList(list):
    """List to support mutations"""

    def __init__(
        self,
        update_factory: Optional[Callable[[Any, int], None]],
        create_factory: Optional[Callable[[Any, int], None]] = None,
        delete_factory: Optional[Callable[[int], None]] = None,
        move_factory: Optional[Callable[[int, int], None]] = None,
        iterable: Iterable = None,
    ):
        self.initialized = False
        # processed = [WatchedDictionary(parent_dict=x, update_factory=update_factory) if isinstance(x, dict) else x for x in iterable]
        super().__init__(iterable)
        self.update_factory = update_factory
        self.create_factory = create_factory
        self.delete_factory = delete_factory
        self.move_factory = move_factory
        self.sync_changes: bool = True

    def __setitem__(self, key: int, value) -> None:
        current = self[key]
        super().__setitem__(key, value)
        if current != value and self.sync_changes:
            self.update_factory(value, key)

    def insert(self, __index: int, __object) -> None:
        super().insert(__index, __object)
        if self.sync_changes:
            self.create_factory(__object, __index)

    def __delitem__(self, key: int) -> None:
        if self.sync_changes:
            self.delete_factory(key)
        super().__delitem__(key)

    def move(self, original_idx: int, new_idx: int) -> None:
        # we don't actually want to send the deletion or insertion
        # as the move handles both of these
        self.sync_changes = False
        del self[original_idx]
        stash = self[original_idx]
        self.insert(new_idx, stash)
        self.move_factory(original_idx, new_idx)
        self.sync_changes = True

    def append(self, __object) -> None:
        self.create_factory(__object, len(self))
        super().append(__object)


class WatchedDictionary(dict):
    """Dictionary to support mutations"""

    def __init__(
        self,
        update_factory: Any,
        # create_factory:Optional[Any] = None,
        # delete_factory:Optional[Any]  = None,
        # parent: Optional["WatchedDictionary"] = None,
        parent_dict: dict,
    ):
        self.update_factory = update_factory
        # don't track updates for initial build
        self.initialized = False
        self.update(**parent_dict)
        # now, all modifications will trigger updates
        self.initialized = True
        self.request_queue = []

    def _trigger_update(self):
        if self.initialized:
            self.update_factory()

    def __setitem__(self, key, val):
        comp = self.get(key, None)
        dict.__setitem__(self, key, val)
        # early exit if no changes
        if comp == val:
            return
        self._trigger_update()

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._trigger_update()

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            if isinstance(v, dict):
                v = WatchedDictionary(parent_dict=v, update_factory=self.update_factory)
            self[k] = v
        self._trigger_update()
