def render(copies):
    if copies < 1 or copies > 64:
        raise ValueError("invalid copies")
    return [bytes(65536) for _ in range(copies)]
