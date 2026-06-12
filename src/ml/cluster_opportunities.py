import re

import numpy as np
import pandas as pd

from src.processing.clean_text import clean_text


STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "work",
    "student",
    "students",
    "opportunity",
    "program",
}


def tokenize(text: object) -> list[str]:
    """Tokenize text into simple lowercase terms for clustering."""
    cleaned = clean_text(text).lower()
    tokens = re.findall(r"[a-z0-9]+", cleaned)
    return [token for token in tokens if len(token) > 2 and token not in STOPWORDS]


def build_cluster_text(row: pd.Series) -> str:
    """Combine fields used to group similar opportunities."""
    fields = [
        "title",
        "organization",
        "description",
        "category",
        "predicted_category",
        "required_skills",
    ]
    return " ".join(clean_text(row.get(field, "")) for field in fields)


def build_vocabulary(texts: list[str], max_features: int = 50) -> list[str]:
    """Build a deterministic vocabulary from the most frequent terms."""
    term_counts = {}

    for text in texts:
        for token in tokenize(text):
            term_counts[token] = term_counts.get(token, 0) + 1

    sorted_terms = sorted(term_counts.items(), key=lambda item: (-item[1], item[0]))
    return [term for term, _ in sorted_terms[:max_features]]


def vectorize_texts(texts: list[str], vocabulary: list[str]) -> np.ndarray:
    """Convert texts into normalized bag-of-words vectors."""
    if not texts or not vocabulary:
        return np.zeros((len(texts), 0))

    vocabulary_index = {term: index for index, term in enumerate(vocabulary)}
    vectors = np.zeros((len(texts), len(vocabulary)), dtype=float)

    for row_index, text in enumerate(texts):
        for token in tokenize(text):
            if token in vocabulary_index:
                vectors[row_index, vocabulary_index[token]] += 1.0

    norms = np.linalg.norm(vectors, axis=1)
    non_zero_rows = norms > 0
    vectors[non_zero_rows] = vectors[non_zero_rows] / norms[non_zero_rows, None]
    return vectors


def fit_kmeans(
    vectors: np.ndarray,
    n_clusters: int = 3,
    max_iterations: int = 50,
) -> np.ndarray:
    """Cluster vectors with a small deterministic K-Means implementation."""
    if len(vectors) == 0:
        return np.array([], dtype=int)

    if vectors.shape[1] == 0:
        return np.zeros(len(vectors), dtype=int)

    cluster_count = min(n_clusters, len(vectors))
    centroids = vectors[:cluster_count].copy()
    labels = np.zeros(len(vectors), dtype=int)

    for _ in range(max_iterations):
        distances = np.linalg.norm(vectors[:, None, :] - centroids[None, :, :], axis=2)
        new_labels = np.argmin(distances, axis=1)

        if np.array_equal(labels, new_labels):
            break

        labels = new_labels

        for cluster_id in range(cluster_count):
            cluster_vectors = vectors[labels == cluster_id]
            if len(cluster_vectors) > 0:
                centroids[cluster_id] = cluster_vectors.mean(axis=0)

    return labels


def describe_clusters(
    vectors: np.ndarray,
    labels: np.ndarray,
    vocabulary: list[str],
    top_terms: int = 3,
) -> dict[int, str]:
    """Create readable labels from the strongest terms in each cluster."""
    descriptions = {}

    for cluster_id in sorted(set(labels)):
        cluster_vectors = vectors[labels == cluster_id]
        if len(cluster_vectors) == 0 or len(vocabulary) == 0:
            descriptions[int(cluster_id)] = f"cluster_{cluster_id}"
            continue

        mean_vector = cluster_vectors.mean(axis=0)
        top_indexes = np.argsort(mean_vector)[::-1][:top_terms]
        keywords = [vocabulary[index] for index in top_indexes if mean_vector[index] > 0]
        descriptions[int(cluster_id)] = ", ".join(keywords) or f"cluster_{cluster_id}"

    return descriptions


def apply_opportunity_clustering(
    dataframe: pd.DataFrame,
    n_clusters: int = 3,
) -> pd.DataFrame:
    """Add K-Means cluster columns to the opportunities dataset."""
    clustered = dataframe.copy()

    if clustered.empty:
        clustered["cluster_id"] = []
        clustered["cluster_label"] = []
        clustered["cluster_keywords"] = []
        return clustered

    texts = [build_cluster_text(row) for _, row in clustered.iterrows()]
    vocabulary = build_vocabulary(texts)
    vectors = vectorize_texts(texts, vocabulary)
    labels = fit_kmeans(vectors, n_clusters=n_clusters)
    descriptions = describe_clusters(vectors, labels, vocabulary)

    clustered["cluster_id"] = labels
    clustered["cluster_keywords"] = [
        descriptions[int(cluster_id)] for cluster_id in labels
    ]
    clustered["cluster_label"] = [
        f"cluster_{int(cluster_id)}: {descriptions[int(cluster_id)]}"
        for cluster_id in labels
    ]

    return clustered
