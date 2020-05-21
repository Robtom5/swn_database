import pytest


@pytest.fixture
def sql_connection():
    return MockSQLConn()


class MockSQLConn():
    def __init__(self):
        self.results = None
        self._queries = []
        self.rolledback = False
        self.committed = False

    @property
    def database_path(self):
        return "some_path"

    def set_execute_read_results(self, results):
        self.results = results

    def execute_read_query(self, query, suppress=False):
        self._queries.append(query)
        return self.results.pop(0)

    def execute_query(self, query):
        self._queries.append(query)

    def get_queries(self):
        return self._queries

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolledback = True


def trialMethod():
    pass
