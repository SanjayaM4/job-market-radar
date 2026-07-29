import re

from sentence_transformers import SentenceTransformer, util

# Loaded once and reused - loading this model is the slow part, so we don't
# want to do it per-posting.
_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def strip_html(text: str) -> str:
    """Greenhouse descriptions come through as HTML - strip tags before embedding."""
    if not text:
        return ""
    return re.sub(r"<[^>]+>", " ", text)


def compute_match_score(profile_text: str, posting_text: str) -> float:
    """
    Returns a cosine similarity score between 0 and 1 (roughly) comparing
    a profile description against a posting's title + description.
    Higher = more semantically similar.
    """
    model = get_model()
    profile_embedding = model.encode(profile_text, convert_to_tensor=True)
    posting_embedding = model.encode(strip_html(posting_text), convert_to_tensor=True)
    similarity = util.cos_sim(profile_embedding, posting_embedding)
    return float(similarity.item())
