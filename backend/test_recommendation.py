from services.recommendation import calculate_skill_match

user_skill_ids = {2}

job_skills = [
    {
        "skill_id": 2,
        "is_required": True,
        "required_level": "Advanced",
        "user_level": "Intermediate",
    },
    {
        "skill_id": 1,
        "is_required": False,
        "required_level": "Intermediate",
        "user_level": None,
    },
]

result = calculate_skill_match(user_skill_ids, job_skills)

assert result["match_score"] == 40.0
assert result["matched_required_skills"] == [2]
assert result["missing_required_skills"] == []
assert result["matched_optional_skills"] == []
assert result["missing_optional_skills"] == [1]

print("All tests passed!")
print(result)