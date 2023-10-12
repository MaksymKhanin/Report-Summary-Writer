import textwrap
import nltk
from nltk.tokenize import sent_tokenize


nltk.download('punkt')


class ChunksSplitter:

    def split_text_to_chunks(text, max_tokens_per_chunk=2000):

        # Assuming paragraphs are separated by two newline characters
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ''

        for paragraph in paragraphs:
            sentences = sent_tokenize(paragraph)
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 <= max_tokens_per_chunk:  # +1 for space
                    current_chunk += sentence + ' '
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence + ' '

        if current_chunk:  # Append the last remaining chunk
            chunks.append(current_chunk.strip())

        return chunks
