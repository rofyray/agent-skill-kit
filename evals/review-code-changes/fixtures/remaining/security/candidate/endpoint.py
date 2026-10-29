def render(copies):
    if copies < 1:
        raise ValueError("invalid copies")
    return [bytes(65536) for _ in range(copies)]
