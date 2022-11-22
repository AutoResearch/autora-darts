__all__ = ["weber_filter"]


def weber_filter(values):
    return filter(lambda s: s[0] <= s[1], values)
