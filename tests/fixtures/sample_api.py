"""API endpoints for constitution testing."""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional


router = APIRouter(prefix="/api/v1")


class TestSubmitRequest(BaseModel):
    """Request model for constitution test submission."""

    answers: List[int] = Field(..., description="List of 30 answers (1-5 scale)", min_length=30, max_length=30)
    user_id: Optional[str] = Field(None, description="Optional user ID for tracking")
    device_id: Optional[str] = Field(None, description="Device identifier")


class TestSubmitResponse(BaseModel):
    """Response model for constitution test submission."""

    result_id: str = Field(..., description="Unique result identifier")
    primary_constitution: str = Field(..., description="Primary constitution type")
    primary_constitution_name: str = Field(..., description="Chinese name of constitution")
    secondary_constitutions: List[dict] = Field(default_factory=list, description="Secondary constitutions")
    scores: dict = Field(..., description="All constitution scores")


class ConstitutionResponse(BaseModel):
    """Response model for constitution result retrieval."""

    result_id: str
    user_id: Optional[str]
    primary_constitution: str
    primary_constitution_name: str
    secondary_constitutions: List[dict]
    scores: dict
    characteristics: dict
    regulation_principles: dict
    created_at: str


@router.post(
    "/test/submit",
    response_model=TestSubmitResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit constitution test",
    description="Submit 30-question constitution test and receive analysis results"
)
async def submit_test(request: TestSubmitRequest) -> TestSubmitResponse:
    """Submit constitution test answers and get results.

    Args:
        request: Test submission request with 30 answers

    Returns:
        Constitution analysis result with primary type and scores

    Raises:
        HTTPException: If answers validation fails
    """
    # Validate answer count
    if len(request.answers) != 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Expected 30 answers, got {len(request.answers)}"
        )

    # Validate answer range
    invalid_answers = [a for a in request.answers if a < 1 or a > 5]
    if invalid_answers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All answers must be between 1 and 5"
        )

    # Calculate scores (simplified logic)
    scores = {
        "peace": 25.0,
        "qi_deficiency": 85.0,
        "yang_deficiency": 35.0,
        "yin_deficiency": 20.0,
        "phlegm_damp": 15.0,
        "damp_heat": 10.0,
        "blood_stasis": 5.0,
        "qi_depression": 25.0,
        "special": 10.0
    }

    return TestSubmitResponse(
        result_id="test-123",
        primary_constitution="qi_deficiency",
        primary_constitution_name="气虚质",
        secondary_constitutions=[
            {"type": "yang_deficiency", "name": "阳虚质", "score": 35.0}
        ],
        scores=scores
    )


@router.get(
    "/result/{result_id}",
    response_model=ConstitutionResponse,
    summary="Get test result",
    description="Retrieve detailed constitution test result by ID"
)
async def get_result(result_id: str) -> ConstitutionResponse:
    """Get constitution test result by ID.

    Args:
        result_id: Unique result identifier

    Returns:
        Detailed constitution result with characteristics and recommendations
    """
    # Mock response
    return ConstitutionResponse(
        result_id=result_id,
        user_id="user-123",
        primary_constitution="qi_deficiency",
        primary_constitution_name="气虚质",
        secondary_constitutions=[
            {"type": "yang_deficiency", "name": "阳虚质", "score": 35.0}
        ],
        scores={
            "peace": 25.0,
            "qi_deficiency": 85.0,
            "yang_deficiency": 35.0,
            "yin_deficiency": 20.0,
            "phlegm_damp": 15.0,
            "damp_heat": 10.0,
            "blood_stasis": 5.0,
            "qi_depression": 25.0,
            "special": 10.0
        },
        characteristics={
            "title": "气虚质的典型表现",
            "items": [
                "疲乏气短，活动后加重",
                "容易出汗，稍动即汗",
                "容易感冒，免疫力低",
                "肌肉松软，舌淡苔白"
            ]
        },
        regulation_principles={
            "diet": ["多食糯米、大枣、山药、鸡肉"],
            "exercise": ["选择柔和运动，避免大汗淋漓"],
            "lifestyle": ["规律作息，避免熬夜"],
            "emotion": ["保持心情舒畅，避免过度思虑"]
        },
        created_at="2025-01-13T10:30:00Z"
    )
