"""Pydantic request/response models for the Pi-Scope API.

Every field is documented and validated so the auto-generated OpenAPI schema
(served at ``/docs``) is a faithful, self-describing contract for the frontend.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.dimensions import NB_BASE_DIMENSIONS


class VariableIn(BaseModel):
    """A single variable submitted for analysis.

    Attributes:
        symbol: Short identifier (must be unique within a request).
        exponents: Exponents over the SI base dimensions, in canonical order
            (M, L, T, Θ, I, N, J). Shorter vectors are zero-padded.
        latex: Optional LaTeX rendering of the symbol.
        name: Optional human-readable name.
    """

    model_config = ConfigDict(extra="forbid")

    symbol: str = Field(..., min_length=1, max_length=32, examples=["rho"])
    exponents: list[float] = Field(..., examples=[[1, -3, 0]])
    latex: str | None = Field(default=None, examples=[r"\rho"])
    name: str | None = Field(default=None, examples=["Density"])

    @field_validator("exponents")
    @classmethod
    def _check_length(cls, value: list[float]) -> list[float]:
        """Reject exponent vectors longer than the number of base dimensions.

        Args:
            value: The submitted exponent vector.

        Returns:
            The validated vector.

        Raises:
            ValueError: If the vector has more than seven entries.
        """
        if len(value) > NB_BASE_DIMENSIONS:
            raise ValueError(
                f"At most {NB_BASE_DIMENSIONS} exponents are allowed, got {len(value)}."
            )
        return value


class SolveRequest(BaseModel):
    """Body of a ``POST /api/pi/solve`` request.

    Attributes:
        variables: The variables to analyse (two or more).
        integerize: Whether to scale group exponents to the smallest integers.
    """

    model_config = ConfigDict(extra="forbid")

    variables: list[VariableIn] = Field(..., min_length=2)
    integerize: bool = True


class PiGroupOut(BaseModel):
    """A single dimensionless group in an API response.

    Attributes:
        index: 1-based group index.
        exponents: Integer exponent applied to each input variable (input order).
        latex: LaTeX rendering of the group.
        ascii: Plain-text rendering of the group.
    """

    index: int
    exponents: list[int]
    latex: str
    ascii: str


class PiResultOut(BaseModel):
    """Full response of a Pi-theorem computation.

    Attributes:
        variables: Variable symbols in input order (matrix columns).
        base_symbols: Active base-dimension symbols (matrix rows).
        matrix: Dimensional matrix (rows over active dimensions).
        rank: Rank of the dimensional matrix.
        n_variables: Number of variables analysed.
        n_groups: Number of independent dimensionless groups.
        groups: The computed groups.
        product_latex: LaTeX of the product of all groups, if more than one.
    """

    variables: list[str]
    base_symbols: list[str]
    matrix: list[list[int]]
    rank: int
    n_variables: int
    n_groups: int
    groups: list[PiGroupOut]
    product_latex: str | None = None


class BaseDimensionInfo(BaseModel):
    """Metadata describing one SI base dimension (for the frontend UI).

    Attributes:
        symbol: Physics symbol (e.g. ``"M"``).
        name: snake_case machine name (e.g. ``"mass"``).
        si_unit: Coherent SI unit (e.g. ``"kg"``).
        label_en: English label.
        label_fr: French label.
    """

    symbol: str
    name: str
    si_unit: str
    label_en: str
    label_fr: str


class VariableLibraryEntry(BaseModel):
    """A predefined variable from the curated library.

    Attributes:
        symbol: Short identifier.
        name_en: English name.
        name_fr: French name.
        si_unit: Coherent SI unit.
        exponents: Exponents over the SI base dimensions (canonical order).
        latex: LaTeX rendering of the symbol.
        description_en: Optional English physical description.
        description_fr: Optional French physical description.
    """

    symbol: str
    name_en: str
    name_fr: str
    si_unit: str
    exponents: list[float]
    latex: str
    description_en: str | None = None
    description_fr: str | None = None


class LibraryCategory(BaseModel):
    """A physics domain grouping several library variables.

    Attributes:
        id: Stable identifier (slug), e.g. ``"fluid_mechanics"``.
        name_en: English category name.
        name_fr: French category name.
        variables: Variables belonging to this category.
    """

    id: str
    name_en: str
    name_fr: str
    variables: list[VariableLibraryEntry]


class LibraryResponse(BaseModel):
    """Response of ``GET /api/library``.

    Attributes:
        base_dimensions: The seven SI base dimensions and their metadata.
        categories: All library categories with their variables.
    """

    base_dimensions: list[BaseDimensionInfo]
    categories: list[LibraryCategory]


class WorkedExample(BaseModel):
    """A preloaded, citeable case study.

    Attributes:
        id: Stable identifier (slug), e.g. ``"chen_1990"``.
        title_en: English title.
        title_fr: French title.
        description_en: English description / context.
        description_fr: French description / context.
        reference: Bibliographic reference, if any.
        variables: The variables that make up the example.
    """

    id: str
    title_en: str
    title_fr: str
    description_en: str
    description_fr: str
    reference: str | None = None
    variables: list[VariableIn]
