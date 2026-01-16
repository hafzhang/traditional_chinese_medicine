"""Sample valid Python file for testing."""
from typing import List, Dict, Optional


def calculate_constitution_score(answers: List[int]) -> Dict[str, float]:
    """Calculate constitution scores from questionnaire answers.

    Args:
        answers: List of 30 answers (1-5 scale)

    Returns:
        Dictionary with scores for each constitution type
    """
    scores = {
        "peace": 0.0,
        "qi_deficiency": 0.0,
        "yang_deficiency": 0.0,
        "yin_deficiency": 0.0,
        "phlegm_damp": 0.0,
        "damp_heat": 0.0,
        "blood_stasis": 0.0,
        "qi_depression": 0.0,
        "special": 0.0
    }

    # Calculate raw scores
    for answer in answers:
        scores["qi_deficiency"] += answer * 0.1

    # Convert to percentage
    for key in scores:
        scores[key] = min(100, scores[key] * 2.5)

    return scores


class ConstitutionAnalyzer:
    """Analyzes user constitution type based on answers."""

    def __init__(self, version: str = "1.0.0"):
        """Initialize the analyzer.

        Args:
            version: Analyzer version string
        """
        self.version = version
        self.score_threshold = {
            "primary": 40,
            "secondary": 30,
            "peace": 60
        }

    def analyze(self, answers: List[int]) -> Dict[str, any]:
        """Analyze answers and determine constitution type.

        Args:
            answers: List of questionnaire answers

        Returns:
            Analysis result with primary constitution and scores
        """
        scores = calculate_constitution_score(answers)
        primary = self._determine_primary(scores)
        secondary = self._determine_secondary(scores, primary)

        return {
            "primary": primary,
            "secondary": secondary,
            "scores": scores
        }

    def _determine_primary(self, scores: Dict[str, float]) -> str:
        """Determine primary constitution type."""
        max_score = 0
        primary_type = "peace"

        for constitution, score in scores.items():
            if score > max_score:
                max_score = score
                primary_type = constitution

        # Special case for peace constitution
        if scores["peace"] >= 60:
            return "peace"

        return primary_type

    def _determine_secondary(self, scores: Dict[str, float], primary: str) -> List[Dict]:
        """Determine secondary constitution types."""
        secondary = []

        for constitution, score in scores.items():
            if constitution != primary and score >= 30:
                secondary.append({
                    "type": constitution,
                    "score": score
                })

        return secondary
