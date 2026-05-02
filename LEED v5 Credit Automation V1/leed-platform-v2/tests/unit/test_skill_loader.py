"""Tests for the skill loader and adapter."""

from pathlib import Path

from agents.skill_adapter import SkillLoader


SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills"


def test_load_mr_c3_skill():
    """MRc3 skill manifest should load correctly."""
    loader = SkillLoader(SKILLS_DIR)
    manifest = loader.load("mr_c3_low_emitting")

    assert manifest.credit_code == "MRc3"
    assert manifest.credit_name == "Low-Emitting Materials"
    assert manifest.max_points == 3
    assert manifest.is_prerequisite is False
    assert manifest.requires_human_review is True
    assert len(manifest.workflow_steps) == 8
    assert len(manifest.agents) == 3
    assert len(manifest.validators) == 4


def test_load_we_p2_skill():
    """WEp2 skill manifest should load correctly."""
    loader = SkillLoader(SKILLS_DIR)
    manifest = loader.load("we_p2_water_min")

    assert manifest.credit_code == "WEp2"
    assert manifest.is_prerequisite is True
    assert manifest.max_points == 0
    assert len(manifest.workflow_steps) == 9


def test_load_by_credit_code():
    """Loading by credit code should find the correct skill."""
    loader = SkillLoader(SKILLS_DIR)
    manifest = loader.load_by_credit_code("MRc3")

    assert manifest.id == "leed.mr_c3.low_emitting_materials"


def test_list_skills():
    """Should list all available skills."""
    loader = SkillLoader(SKILLS_DIR)
    skills = loader.list_skills()

    assert len(skills) >= 2
    codes = {s.credit_code for s in skills}
    assert "MRc3" in codes
    assert "WEp2" in codes


def test_get_instructions():
    """Should load instructions.md content."""
    loader = SkillLoader(SKILLS_DIR)
    instructions = loader.get_instructions("mr_c3_low_emitting")

    assert "Low-Emitting Materials" in instructions
    assert "GREENGUARD" in instructions


def test_get_input_schema():
    """Should load input_schema.json."""
    loader = SkillLoader(SKILLS_DIR)
    schema = loader.get_input_schema("mr_c3_low_emitting")

    assert schema.get("type") == "object"
    assert "product_datasheets" in schema.get("properties", {})
