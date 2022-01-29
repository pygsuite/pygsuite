from pygsuite.drive.query import Connector, Operator, QueryString, QueryStringGroup, QueryTerm

condition1 = QueryString(QueryTerm.WRITERS, Operator.IN, "test@gmail.com")
condition2 = QueryString(QueryTerm.TEXT, Operator.CONTAINS, "something")

query = QueryStringGroup([condition1, condition2], [Connector.AND])
print(query.formatted)
