# Preload the emoji map to memory, so we don't have to do it for each function call
with open("./misc/emojis.csv") as file:
    _emoji_names_map = {}

    for line in file.readlines():
        emoji, name = line.split(", ", maxsplit=1)
        # Clean up the name string
        name = name.lstrip("\"\n").rstrip("\"\n")
        # Map the emoji to it's name
        _emoji_names_map[emoji] = name

def cleanup(text):
    """Cleans up the given text by replacing emojis with their names."""
    cleaned_up_text = text

    for character in text:
        if character in _emoji_names_map:
            emoji_name = _emoji_names_map[character]
            cleaned_up_text = cleaned_up_text.replace(character, f"<{emoji_name}> ")

    return cleaned_up_text
