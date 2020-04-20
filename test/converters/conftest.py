import pytest

@pytest.fixture
def sql_connection():
    return MockSQLConn()    

class MockSQLConn():
    def __init__(self):
        self.results = None
        self._queries = []

    @property
    def database_path(self):
        return "some_path"

    def set_execute_read_results(self, results):
        self.results = results

    def execute_read_query(self, query):
        self._queries.append(query)
        return self.results.pop(0)

    def execute_query(self, query):
        self._queries.append(query)

    def get_queries(self):
        return self._queries

def trialMethod():
    pass