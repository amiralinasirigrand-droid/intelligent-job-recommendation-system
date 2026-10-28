
from services.recommendation import calculate_skill_match


def test_all_skills_meet_required_levels():
    job_skills = [
        {
            "skill_id": 1,
            "name": "FastAPI",
            "is_required": True,
            "required_level": "advanced",
            "user_level": "advanced",
        },
        {
            "skill_id": 2,
            "name": "Python",
            "is_required": False,
            "required_level": "intermediate",
            "user_level": "intermediate",
        },
    ]

    result = calculate_skill_match([1, 2], job_skills)

    assert result["match_score"] == 100.0
    assert result["missing_required_skills"] == []
    assert result["missing_optional_skills"] == []


def test_missing_required_skill_with_optional_skill_present():
    job_skills = [
        {
            "skill_id": 1,
            "name": "FastAPI",
            "is_required": True,
            "required_level": "advanced",
            "user_level": None,
        },
        {
            "skill_id": 2,
            "name": "Python",
            "is_required": False,
            "required_level": "intermediate",
            "user_level": "intermediate",
        },
    ]

    result = calculate_skill_match([2], job_skills)

    assert result["match_score"] == 20.0
    assert result["missing_required_skills"] == [1]
    assert result["matched_optional_skills"] == [2]


def test_beginner_level_gets_partial_score():
    job_skills = [
        {
            "skill_id": 1,
            "name": "Python",
            "is_required": True,
            "required_level": "advanced",
            "user_level": "beginner",
        }
    ]

    result = calculate_skill_match([1], job_skills)

    assert result["match_score"] == 25.0
    assert result["matched_required_skills"] == [1]
    assert result["missing_required_skills"] == []
def test_missing_skills_includes_missing_optional_skills():
    job_skills = [
        {
            "skill_id": 1,
            "name": "Python",
            "is_required": True,
            "required_level": "advanced",
            "user_level": "advanced",
        },
        {
            "skill_id": 2,
            "name": "PostgreSQL",
            "is_required": False,
            "required_level": "intermediate",
            "user_level": None,
        },
    ]

    result = calculate_skill_match([1], job_skills)

    assert result["match_score"] == 80.0
    assert result["missing_required_skills"] == []
    assert result["missing_optional_skills"] == [2]
    assert result["missing_skills"] == [2]


def test_unknown_required_level_does_not_get_full_credit():
    job_skills = [
        {
            "skill_id": 1,
            "name": "Python",
            "is_required": True,
            "required_level": "expert",
            "user_level": "advanced",
        }
    ]

    result = calculate_skill_match([1], job_skills)

    assert result["match_score"] == 0.0
    assert any(
        "unknown required level" in explanation.lower()
        and "no credit" in explanation.lower()
        for explanation in result["explanations"]
    )