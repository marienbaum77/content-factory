import logging
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

logger = logging.getLogger(__name__)

class TextSummarizer:
    def __init__(self):
        self.language = "russian"
        self.sentences_count = 3  # Количество предложений в выжимке

    def _clean_text(self, text: str) -> str:
        """Убирает лишние пробелы и переносы строк"""
        return " ".join(text.split())

    def _fallback_summary(self, text: str) -> str:
        """
        Запасной вариант: берем первые 3 предложения.
        Регулярка ищет точку, воскл. или вопр. знак, за которыми следует пробел и заглавная буква.
        """
        # Разбиваем на предложения (грубо, но надежно)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        # Берем первые 3
        summary = " ".join(sentences[:3])
        return self._clean_text(summary)

    async def summarize(self, text: str) -> str:
        if not text:
            return "Текст отсутствует."

        try:
            # 1. Сначала пробуем умный алгоритм Sumy
            parser = PlaintextParser.from_string(text, Tokenizer(self.language))
            stemmer = Stemmer(self.language)
            summarizer = LsaSummarizer(stemmer)
            summarizer.stop_words = get_stop_words(self.language)

            summary_sentences = summarizer(parser.document, self.sentences_count)
            
            if not summary_sentences:
                # Если Sumy вернула пустоту (бывает на коротких текстах)
                return self._fallback_summary(text)

            summary_text = " ".join([str(sentence) for sentence in summary_sentences])
            return f"🤖 <b>Авто-выжимка:</b>\n{summary_text}"

        except Exception as e:
            logger.error(f"Sumy error: {e}")
            # 2. Если ошибка (например, с NLTK) — берем просто начало текста аккуратно
            return self._fallback_summary(text)