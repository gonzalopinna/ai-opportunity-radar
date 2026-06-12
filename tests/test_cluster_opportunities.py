import unittest

import numpy as np
import pandas as pd

from src.ml.cluster_opportunities import (
    apply_opportunity_clustering,
    build_vocabulary,
    fit_kmeans,
    tokenize,
    vectorize_texts,
)


class ClusterOpportunitiesTests(unittest.TestCase):
    def test_tokenize_removes_short_words_and_stopwords(self):
        tokens = tokenize("AI internship for students with Python and ML")

        self.assertIn("internship", tokens)
        self.assertIn("python", tokens)
        self.assertNotIn("for", tokens)
        self.assertNotIn("ai", tokens)

    def test_vectorize_texts_creates_expected_shape(self):
        texts = ["python machine learning", "startup software engineering"]
        vocabulary = build_vocabulary(texts)
        vectors = vectorize_texts(texts, vocabulary)

        self.assertEqual(vectors.shape[0], 2)
        self.assertEqual(vectors.shape[1], len(vocabulary))

    def test_fit_kmeans_returns_one_label_per_row(self):
        vectors = np.array(
            [
                [1.0, 0.0],
                [0.9, 0.1],
                [0.0, 1.0],
                [0.1, 0.9],
            ]
        )

        labels = fit_kmeans(vectors, n_clusters=2)

        self.assertEqual(len(labels), 4)
        self.assertLessEqual(len(set(labels)), 2)

    def test_apply_opportunity_clustering_adds_cluster_columns(self):
        dataframe = pd.DataFrame(
            [
                {
                    "title": "AI Internship",
                    "organization": "Global AI Lab",
                    "description": "Machine learning research with Python.",
                    "category": "internship",
                    "predicted_category": "internship",
                    "required_skills": "python; machine learning",
                },
                {
                    "title": "Startup Fellowship",
                    "organization": "LaunchPad",
                    "description": "Build software products for startups.",
                    "category": "startup",
                    "predicted_category": "startup",
                    "required_skills": "python; git",
                },
            ]
        )

        clustered = apply_opportunity_clustering(dataframe, n_clusters=2)

        self.assertIn("cluster_id", clustered.columns)
        self.assertIn("cluster_label", clustered.columns)
        self.assertIn("cluster_keywords", clustered.columns)
        self.assertEqual(len(clustered), 2)


if __name__ == "__main__":
    unittest.main()
