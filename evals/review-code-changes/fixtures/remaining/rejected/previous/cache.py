def read(entry, now, load):
    quote, expires = entry
    if now < expires:
        return quote
    return load()
