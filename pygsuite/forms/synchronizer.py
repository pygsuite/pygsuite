from typing import Any, Optional, Iterable

class WatchedList(list):
    '''List to support mutations'''

    def __init__(self, update_factory:Any, create_factory:Optional[Any] = None,
                 delete_factory:Optional[Any]  = None,
                 move_factory:Optional[Any]  = None, iterable:Iterable = None):
        self.initialized = False
        # processed = [WatchedDictionary(parent_dict=x, update_factory=update_factory) if isinstance(x, dict) else x for x in iterable]
        super().__init__(self, iterable)
        self.update_factory = update_factory
        self.create_factory = create_factory
        self.delete_factory = delete_factory
        self.move_factory = move_factory
        self.initialized = True

    def __setitem__(self, key, value):
        current = self[key]
        super().__setitem__(key, value)
        if current != value:
            self.update_factory()

    def __delitem__(self, key):
        self.delete_factory()


class WatchedDictionary(dict):
    '''Dictionary to support mutations'''
    def __init__(self,
                 update_factory:Any,
                 # create_factory:Optional[Any] = None,
                 # delete_factory:Optional[Any]  = None,
                 # parent: Optional["WatchedDictionary"] = None,
                 parent_dict:dict):
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