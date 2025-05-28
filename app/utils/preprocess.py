import re
import string
import emoji # Import the emoji library

def preprocess_tweet(text):
    """Preprocesses the given text.

    Args:
      text: Text to be preprocessed.

    Returns:
      Preprocessed text.
    """

    # Convert to lowercase
    text = text.lower()

    # Convert emojis to text
    text = emoji.demojize(text)

    # URLs are removed
    text = re.sub(r"https?://\S+", "", text)

    # Handles are removed
    text = re.sub(r"@\w+", "", text)

    # Process hashtags
    # First, find all hashtags in the current text
    hashtags = re.findall(r"#\w+", text)
    for hashtag in hashtags:
        # Remove the '#' symbol
        tag_content = hashtag[1:]
        # Split camel case (e.g., #GoodMorning -> Good Morning)
        # This regex looks for a lowercase letter followed by an uppercase letter
        # and inserts a space between them.
        processed_tag = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', tag_content)
        # Replace the original hashtag (e.g., #GoodMorning) with the processed version (e.g., Good Morning)
        # It's important to replace in the 'text' that's being transformed
        text = text.replace(hashtag, processed_tag)
    
    # Normalize elongated words (e.g., "soooo" -> "soo")
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    # Punctuation is removed using string's in-built punctuation method
    # Note: This might remove underscores from demojized emoji text if they are considered punctuation.
    # Depending on the desired outcome for demojized text, this step might need adjustment
    # or to be performed before emoji demojization if underscores in emoji names are to be preserved.
    # For now, following instructions to keep existing punctuation removal logic.
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Normalize whitespace (reduce multiple spaces/tabs to a single space and strip leading/trailing)
    text = re.sub(r'\s+', ' ', text).strip()

    return text
