class EmbedderNode:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def __call__(self, text):
        """
        Convert text into embeddings using the embedding model.
        """
        # Implement embedding logic here
        return []