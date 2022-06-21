# from typing import Any, Optional, Iterable
#
# class WatchedList(list):
#     '''List to support mutations'''
#
#     def __init__(self, update_factory:Any, create_factory:Optional[Any] = None,
#                  delete_factory:Optional[Any]  = None,
#                  move_factory:Optional[Any]  = None, iterable:Iterable = None):
#         super().__init__(self, iterable)
#         self.update_factory = update_factory
#         self.create_factory = create_factory
#         self.delete_factory = delete_factory
#         self.move_factory = move_factory
#
# class WatchedDictionary(dict):
#     '''Dictionary to support mutations'''
#     def __init__(self,
#                  update_factory:Any,
#                  create_factory:Optional[Any] = None,
#                  delete_factory:Optional[Any]  = None,
#                  parent: Optional["WatchedDictionary"] = None,
#                  *args, **kwargs):
#         self.update_factory = update_factory
#         # don't track updates for initial build
#         self.initialized = False
#         self.update(*args, **kwargs)
#         # now, all modifications will trigger updates
#         self.initialized = True
#         self.request_queue = []
#
#     def trigger_update(self):
#         self.request_queue = []
#
#     def __getitem__(self, key):
#         val = dict.__getitem__(self, key)
#         return val
#
#     def __setitem__(self, key, val):
#         if self.update_factory:
#
#         dict.__setitem__(self, key, val)
#
#     def __delitem__(self, key):
#         dict.__delitem__(self, key)
#
#     def __repr__(self):
#         dictrepr = dict.__repr__(self)
#         return '%s(%s)' % (type(self).__name__, dictrepr)
#
#     def update(self, *args, **kwargs):
#         for k, v in dict(*args, **kwargs).iteritems():
#             self[k] = v