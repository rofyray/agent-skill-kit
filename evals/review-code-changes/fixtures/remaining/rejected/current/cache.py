def read(entry, now, load):
    cached_value, expires = entry
    if now < expires:
        return cached_value
    return load()
