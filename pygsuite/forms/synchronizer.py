from typing import Any, Iterable, Callable, overload, Union

try:
    from typing import SupportsIndex
except ImportError:
    SupportsIndex = None  # type: ignore


def generate_function(parent, idx: int, item: Any):
    def new_update_function():
        parent.update_factory(idx, item)

    return new_update_function


class WatchedList(list):
    """List that supports synchronizing changes to remote."""

    def __init__(
        self,
        iterable: Iterable,
        update_factory: Callable[[int, Any], None],
        create_factory: Callable[[Any, "SupportsIndex"], None],
        delete_factory: Callable[[Union["SupportsIndex", slice]], None],
        move_factory: Callable[[int, int], None],
    ):
        self.initialized = False
        self.update_factory = update_factory
        self.create_factory = create_factory
        self.delete_factory = delete_factory
        self.move_factory = move_factory
        super().__init__(iterable)

        self.list = iterable
        self._update_wrappers()
        self.sync_changes: bool = True

    def _update_wrappers(self):
        """Bind all child objects to the appropriate index modification"""
        for idx, item in enumerate(self):
            item._info = WatchedDictionary(
                parent_dict=item._info, update_factory=generate_function(self, idx, item)
            )

    @overload
    def __setitem__(self, key: "SupportsIndex", value: Any) -> None:
        raise NotImplementedError

    @overload
    def __setitem__(self, key: slice, value: Iterable[Any]) -> None:
        raise NotImplementedError

    def __setitem__(self, key: Any, value: Any) -> None:
        current = self[key]
        super().__setitem__(key, value)
        if current != value and self.sync_changes:
            self.update_factory(value, key)

    def insert(self, __index: "SupportsIndex", __object) -> None:
        super().insert(__index, __object)
        if self.sync_changes:
            self.create_factory(__object, __index)
        self._update_wrappers()

    def __delitem__(self, key: Union["SupportsIndex", slice]) -> None:
        if self.sync_changes:
            self.delete_factory(key)
        super().__delitem__(key)
        self._update_wrappers()

    def move(self, original_idx: int, new_idx: int) -> None:
        # we don't actually want to send the deletion or insertion
        # as the move handles both of these
        self.sync_changes = False
        del self[original_idx]
        stash = self[original_idx]
        self.insert(new_idx, stash)
        self.move_factory(original_idx, new_idx)
        self.sync_changes = True
        self._update_wrappers()

    def append(self, __object) -> None:
        self.create_factory(__object, len(self))
        super().append(__object)
        self._update_wrappers()


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
