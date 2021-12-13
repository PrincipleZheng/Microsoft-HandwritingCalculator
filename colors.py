def getColor(gid):
    colors = [
        "red",
        "blue",
        "yellowgreen",
        "gray",
        "green",
        "black",
        "pink",
        "purple",
        "orange",
        "aqua"
        ]
    return colors[(gid - 1) % len(colors)]