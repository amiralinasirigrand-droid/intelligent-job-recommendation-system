
def calculate_skill_match(user_skill_ids, job_skills):
    user_skill_ids = set(user_skill_ids)

    level_scores = {
        "beginner": 25,
        "intermediate": 50,
        "advanced": 100,
    }

    required_skills = [
        skill for skill in job_skills
        if skill["is_required"]
    ]

    optional_skills = [
        skill for skill in job_skills
        if not skill["is_required"]
    ]

    explanations = []

    def calculate_group_score(skills, group_weight):
        if not skills:
            return 0.0

        total_score = 0.0

        for skill in skills:
            skill_id = skill["skill_id"]
            skill_name = skill.get("name", f"Skill {skill_id}")
            user_level = skill.get("user_level")
            required_level = skill.get("required_level")
            is_required = skill["is_required"]

            group_type = "Required" if is_required else "Optional"

            if skill_id not in user_skill_ids:
                explanations.append(
                    f"{group_type} skill '{skill_name}' is missing."
                )
                continue

            if not required_level:
                skill_score = 100.0
                explanations.append(
                    f"{skill_name}: skill is present; no required level was specified."
                )
            else:
                user_score = level_scores.get(
                    user_level.lower() if user_level else "",
                    0
                )
                required_score = level_scores.get(
                    required_level.lower(),
                    0
                )

                if required_score == 0:
                    skill_score = 0.0
                    explanations.append(
                        f"{skill_name}: unknown required level; no credit was applied."
                    )
                else:
                    skill_score = min(
                        user_score / required_score * 100,
                        100.0
                    )

                    if user_score >= required_score:
                        explanations.append(
                            f"{skill_name}: your {user_level} level meets the "
                            f"{required_level} requirement."
                        )
                    else:
                        explanations.append(
                            f"{skill_name}: your {user_level or 'unspecified'} level "
                            f"is below the required {required_level} level."
                        )

            total_score += skill_score

        return (total_score / len(skills)) * (group_weight / 100)

    required_weight = 80.0 if required_skills else 0.0
    optional_weight = 20.0 if optional_skills else 0.0

    if required_skills and not optional_skills:
        required_weight = 100.0
    elif optional_skills and not required_skills:
        optional_weight = 100.0

    required_score = calculate_group_score(
        required_skills,
        required_weight
    )

    optional_score = calculate_group_score(
        optional_skills,
        optional_weight
    )

    match_score = required_score + optional_score

    matched_required = {
        skill["skill_id"]
        for skill in required_skills
        if skill["skill_id"] in user_skill_ids
    }

    missing_required = {
        skill["skill_id"]
        for skill in required_skills
        if skill["skill_id"] not in user_skill_ids
    }

    matched_optional = {
        skill["skill_id"]
        for skill in optional_skills
        if skill["skill_id"] in user_skill_ids
    }

    missing_optional = {
        skill["skill_id"]
        for skill in optional_skills
        if skill["skill_id"] not in user_skill_ids
    }

    return {
        "match_score": round(match_score, 2),
        "matched_skills": sorted(
            matched_required | matched_optional
        ),
        "missing_skills": sorted(
    missing_required | missing_optional
),
        "matched_required_skills": sorted(matched_required),
        "missing_required_skills": sorted(missing_required),
        "matched_optional_skills": sorted(matched_optional),
        "missing_optional_skills": sorted(missing_optional),
        "explanations": explanations,
    }
