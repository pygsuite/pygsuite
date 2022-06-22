from typing import Any, Iterable, Callable, overload, SupportsIndex, Union


class WatchedList(list):
    """List that supports synchronizing changes to remote."""

    def __init__(
        self,
        iterable: Iterable,
        update_factory: Callable[[Any, int], None],
        create_factory: Callable[[Any, SupportsIndex], None],
        delete_factory: Callable[[Union[SupportsIndex, slice]], None],
        move_factory: Callable[[int, int], None],
    ):
        self.initialized = False
        # processed = [WatchedDictionary(parent_dict=x, update_factory=update_factory) if isinstance(x, dict) else x for x in iterable]
        super().__init__(iterable)
        self.update_factory = update_factory
        self.create_factory = create_factory
        self.delete_factory = delete_factory
        self.move_factory = move_factory
        self.sync_changes: bool = True

    @overload
    def __setitem__(self, key: SupportsIndex, value: Any) -> None:
        raise NotImplementedError

    @overload
    def __setitem__(self, key: slice, value: Iterable[Any]) -> None:
        raise NotImplementedError

    def __setitem__(self, key: Any, value: Any) -> None:
        current = self[key]
        super().__setitem__(key, value)
        if current != value and self.sync_changes:
            self.update_factory(value, key)

    def insert(self, __index: SupportsIndex, __object) -> None:
        super().insert(__index, __object)
        if self.sync_changes:
            self.create_factory(__object, __index)

    def __delitem__(self, key: Union[SupportsIndex, slice]) -> None:
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
        update_factory: Callable[[], Any],
        # create_factory:Optional[Any] = None,
        # delete_factory:Optional[Any]  = None,
        # parent: Optional["WatchedDictionary"] = None,
        parent_dict: dict,
    ):
        self.update_factory = update_factory
        # don't track updates for initial build
        self.initialized: bool = False
        self.update(**parent_dict)
        # now, all modifications will trigger updates
        self.initialized = True

    def _trigger_update(self) -> None:
        if self.initialized:
            self.update_factory()

    def __setitem__(self, key, val) -> None:
        comp = self.get(key, None)
        dict.__setitem__(self, key, val)
        # early exit if no changes
        if comp == val:
            return
        self._trigger_update()

    def __delitem__(self, key) -> None:
        dict.__delitem__(self, key)
        self._trigger_update()

    def update(self, *args, **kwargs) -> None:
        for k, v in dict(*args, **kwargs).items():
            if isinstance(v, dict):
                v = WatchedDictionary(parent_dict=v, update_factory=self.update_factory)
            self[k] = v
        self._trigger_update()
