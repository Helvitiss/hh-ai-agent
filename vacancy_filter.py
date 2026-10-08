import re


LANGUAGE_MARKERS = (
    ("1c", re.compile(r"(?<!\w)1[сc](?!\w)")),
    ("c++", re.compile(r"(?<!\w)(?:c\+\+|cpp)(?!\w)")),
    ("c#", re.compile(r"(?<!\w)(?:c#|csharp)(?!\w)")),
    ("python", re.compile(r"(?<!\w)python(?!\w)")),
    ("javascript", re.compile(r"(?<!\w)(?:javascript|js)(?!\w)")),
    ("typescript", re.compile(r"(?<!\w)(?:typescript|ts)(?!\w)")),
    ("java", re.compile(r"(?<!\w)java(?!\w)")),
    ("golang", re.compile(r"(?<!\w)golang(?!\w)")),
    ("rust", re.compile(r"(?<!\w)rust(?!\w)")),
    ("php", re.compile(r"(?<!\w)php(?!\w)")),
    ("ruby", re.compile(r"(?<!\w)ruby(?!\w)")),
    ("swift", re.compile(r"(?<!\w)swift(?!\w)")),
    ("kotlin", re.compile(r"(?<!\w)kotlin(?!\w)")),
    ("scala", re.compile(r"(?<!\w)scala(?!\w)")),
    ("dart", re.compile(r"(?<!\w)dart(?!\w)")),
    ("elixir", re.compile(r"(?<!\w)elixir(?!\w)")),
    ("haskell", re.compile(r"(?<!\w)haskell(?!\w)")),
    ("dotnet", re.compile(r"(?<!\w)(?:\.net|dotnet)(?!\w)")),
)


def title_rejection_reason(
    title: str, excluded_positions: tuple[str, ...]
) -> str | None:
    normalized = title.casefold()
    return next(
        (
            word
            for word in excluded_positions
            if word.casefold() in normalized
        ),
        None,
    )


def title_language_rejection_reason(
    title: str, preferred_technologies: tuple[str, ...]
) -> str | None:
    normalized_title = title.casefold().replace("с++", "c++").replace("с#", "c#")
    preferred = {
        language
        for technology in preferred_technologies
        for language, marker in LANGUAGE_MARKERS
        if marker.search(technology.casefold().replace("с++", "c++").replace("с#", "c#"))
    }
    for language, marker in LANGUAGE_MARKERS:
        if marker.search(normalized_title) and language not in preferred:
            return language
    return None


def vacancy_rejection_reason(
    *,
    title: str,
    company: str,
    description: str,
    excluded_positions: tuple[str, ...],
    excluded_companies: tuple[str, ...],
    excluded_keywords: tuple[str, ...],
    preferred_technologies: tuple[str, ...] = (),
) -> str | None:
    title_match = title_rejection_reason(title, excluded_positions)
    if title_match:
        return f"position:{title_match}"
    language_match = title_language_rejection_reason(title, preferred_technologies)
    if language_match:
        return f"language:{language_match}"
    normalized_company = company.casefold()
    company_match = next(
        (term for term in excluded_companies if term.casefold() in normalized_company),
        None,
    )
    if company_match:
        return f"company:{company_match}"
    normalized_description = description.casefold()
    keyword_match = next(
        (term for term in excluded_keywords if term.casefold() in normalized_description),
        None,
    )
    return f"keyword:{keyword_match}" if keyword_match else None
