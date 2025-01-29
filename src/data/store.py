class DataStore:
    """A simple key-value store that stores data in memory."""

    def __init__(self, db: dict) -> None:
        """Initialize the data store with the specified database."""
        self.db = db

    def get(self, key: str) -> str:
        """Retrieve the value associated with the specified key from the data store."""
        return self.db.get(key)

    def set(self, key: str, value: str) -> None:
        """Store the specified key-value pair in the data store."""
        self.db.set(key, value)
