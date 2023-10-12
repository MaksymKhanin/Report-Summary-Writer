from transformers import BertTokenizer
import os
from transformers import pipeline
import nltk
import textwrap
nltk.download('punkt')


os.environ["CUDA_VISIBLE_DEVICES"] = "0"


class TextSummarizer:

    def get_summary_from_text(txt):
        tokenizer = BertTokenizer.from_pretrained(
            'ProsusAI/finbert', model_max_length=512)

        chunks = textwrap.wrap(txt, 1500)

        summarizer = pipeline(task="summarization",
                              model="facebook/bart-large-cnn")

        summary = ""

        for chunk in chunks:
            summary_text = summarizer(chunk, max_length=50, min_length=5, do_sample=False)[
                0]['summary_text']
            summary += f"\n{summary_text}"

        print(summary)

        return summary
