import json
import os
from typing import Dict, List, Optional

from sentence_transformers import SentenceTransformer, util

FAQ_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "faqs.json")


class FAQService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.faqs: List[Dict] = []
        self.faq_embeddings = None
        self._load_faqs()
        self._compute_faq_embeddings()

    def _load_faqs(self):
        try:
            with open(FAQ_FILE_PATH, "r") as f:
                self.faqs = json.load(f)
        except FileNotFoundError:
            print(f"Error: FAQ file not found at {FAQ_FILE_PATH}")
            self.faqs = [
                {
                    "question": "What is this chatbot?",
                    "answer": "This is a FAQ chatbot that uses semantic search to find answers to your questions.",
                },
                {
                    "question": "How does it work?",
                    "answer": "It uses sentence embeddings to find the most similar question and returns the corresponding answer.",
                },
                {
                    "question": "Who created this chatbot?",
                    "answer": "This chatbot was created as a demonstration of semantic search for FAQs.",
                },
            ]
            print(f"Using default FAQs as file was not found at {FAQ_FILE_PATH}")

    def _compute_faq_embeddings(self):
        if self.faqs:
            questions = [faq["question"] for faq in self.faqs]
            self.faq_embeddings = self.model.encode(questions, convert_to_tensor=True)
        else:
            self.faq_embeddings = None

    def get_best_answer(
        self, user_query: str, similarity_threshold: float = 0.5
    ) -> Optional[Dict]:
        if not self.faqs or self.faq_embeddings is None:
            return None

        query_embedding = self.model.encode(user_query, convert_to_tensor=True)

        cosine_scores = util.pytorch_cos_sim(query_embedding, self.faq_embeddings)

        best_match_idx = cosine_scores.argmax().item()
        best_score = cosine_scores[0, best_match_idx].item()

        if best_score >= similarity_threshold:
            return {
                "question": self.faqs[best_match_idx]["question"],
                "answer": self.faqs[best_match_idx]["answer"],
                "score": best_score,
            }
        return None
