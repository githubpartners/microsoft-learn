"""
AI-Powered Issue Analysis Module

Uses intelligent analysis to:
1. Extract intent and context from issue text
2. Identify specific problems and solutions
3. Generate context-aware PR changes
4. Determine confidence levels for automation
"""

import re
import json


# ─────────────────────────────────────────────────────────────────
# Template noise stripping
# The MS Learn issue forms include literal scaffolding text (checkboxes,
# section headers, placeholders) that should NOT count toward specificity
# or be extracted as the user's "current/desired" state.
# ─────────────────────────────────────────────────────────────────
_TEMPLATE_NOISE_PATTERNS = [
    # Section headers
    r"^.*which of the ms learn modules from the dropdown.*?\?\s*$",
    r"^.*additional information\s*$",
    r"^.*information about the requested update\s*$",
    # Checkbox options (filled or unfilled)
    r"-?\s*\[[ x]\]\s*fix a broken user experience[^\n]*",
    r"-?\s*\[[ x]\]\s*update incorrect information[^\n]*",
    r"-?\s*\[[ x]\]\s*add new content to the module[^\n]*",
    r"-?\s*\[[ x]\]\s*some other request[^\n]*",
    # Bare option lines (when the user didn't even check a box)
    r"^\s*-?\s*fix a broken user experience[^\n]*$",
    r"^\s*-?\s*update incorrect information[^\n]*$",
    r"^\s*-?\s*add new content to the module[^\n]*$",
    r"^\s*-?\s*some other request[^\n]*$",
    # Placeholders / "no response" answers
    r"\[replace_with[^\]]*\]",
    r"^\s*[*_~`]*\s*no response\s*[*_~`]*\s*$",
    r"^\s*none\s*$",
]


def _strip_template_noise(text):
    """Remove MS Learn issue-template scaffolding so it doesn't pollute analysis."""
    if not text:
        return ""
    cleaned = text
    for pat in _TEMPLATE_NOISE_PATTERNS:
        cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
    # Collapse multiple blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _is_effectively_empty(text):
    """True if, after stripping template noise, there is no real user content."""
    return len(_strip_template_noise(text or "").split()) < 5


def _module_selected_without_update_details(body):
    """True when the issue form names a module but its details field is empty."""
    if not body:
        return False

    module_match = re.search(
        r"which of the ms learn modules from the dropdown.*?\?\s*"
        r"(?P<module>.*?)\s*#+\s*additional information",
        body,
        flags=re.IGNORECASE | re.DOTALL,
    )
    details_match = re.search(
        r"#+\s*information about the requested update\s*(?P<details>.*)$",
        body,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not module_match or not details_match:
        return False

    module = module_match.group("module").strip(" \t\r\n*_~`")
    details = details_match.group("details").strip(" \t\r\n*_~`")
    has_module = bool(module) and module.lower() not in {"none", "no response"}
    has_details = bool(details) and details.lower() not in {"none", "no response"}
    return has_module and not has_details


def is_skills_exercise_issue(issue):
    """Return whether user-authored text routes to the Skills exercise team."""
    title = issue.get("title") or ""
    body = _strip_template_noise(issue.get("body") or "")
    user_text = f"{title}\n{body}"
    return bool(
        re.search(
            r"\bgithub\s+skills\b|\bskills(?:[-/][a-z0-9]+)+\b",
            user_text,
            re.IGNORECASE,
        )
        or re.search(r"\bexercises?\b", user_text, re.IGNORECASE)
    )


class IssueAnalyzer:
    """Intelligent issue analysis without external AI dependencies"""
    
    def __init__(self, title, body):
        self.title = title
        # Keep the raw body for length/reporting, but analyze on the cleaned text
        self.body = body
        self.cleaned_body = _strip_template_noise(body or "")
        self.full_text = f"{title}\n{self.cleaned_body}".lower()
        self.analysis = {}
    
    def analyze(self):
        """Perform comprehensive issue analysis"""
        # Build analysis in two passes to avoid circular references
        # First pass: gather all information
        self.analysis = {
            "issue_type": self._detect_issue_type(),
            "specificity_score": self._calculate_specificity(),
            "context_level": self._extract_context(),
            "problem_statement": self._extract_problem(),
            "proposed_fix": self._extract_proposed_fix(),
        }
        
        # Second pass: calculate confidence and actionability 
        # (these depend on the analysis from the first pass)
        self.analysis["confidence"] = self._calculate_confidence()
        self.analysis["actionability"] = self._assess_actionability()
        
        return self.analysis
    
    def _detect_issue_type(self):
        """Detect what type of issue this is"""
        types = []
        
        if any(x in self.full_text for x in ["incorrect", "wrong", "wrong answer", "wrong response", "not correct", "inaccurate"]):
            types.append("incorrect_content")
        
        if any(x in self.full_text for x in ["missing", "not there", "should have", "need to add"]):
            types.append("missing_content")
        
        if any(x in self.full_text for x in ["confusing", "unclear", "hard to understand", "difficult", "misleading", "misrepresent"]):
            types.append("clarity_issue")
        
        if any(x in self.full_text for x in ["typo", "spelling", "grammar", "punctuation"]):
            types.append("typo_or_grammar")
        
        if any(x in self.full_text for x in ["outdated", "old", "deprecated", "no longer", "incorrect information"]):
            types.append("outdated_content")
        
        if any(x in self.full_text for x in ["broken link", "404", "doesn't work", "link error"]):
            types.append("broken_link")
        
        if any(x in self.full_text for x in ["example", "code", "sample"]):
            types.append("code_related")
        
        return types if types else ["general_feedback"]
    
    def _calculate_specificity(self):
        """Score how specific and actionable the issue is (0-100)"""
        score = 0
        
        # Has specific section mentioned (+25)
        if any(x in self.full_text for x in ["unit", "module", "section", "chapter", "knowledge check", "exercise", "lab", "assessment", "check your knowledge"]):
            score += 25
        
        # Has exact location/number (+20)
        if re.search(r'(question|q)\s*(\d+|[a-z])', self.full_text):
            score += 20
        if re.search(r'(line|paragraph)\s*(\d+)', self.full_text):
            score += 20
        
        # Describes current vs desired state (+30)
        if any(x in self.full_text for x in ["current", "should be", "instead of", "currently"]):
            score += 30
        elif any(x in self.full_text for x in ["says", "shows", "displays", "marked as", "written", "described"]):
            score += 20
        
        # Has concrete examples or quoted text (+15)
        if re.search(r'"[^"]{5,}"', self.full_text) or re.search(r"'[^']{5,}'", self.full_text):
            score += 15
        # Also credit parenthetical content like (Option 1), (Correct), etc.
        elif re.search(r'\([^)]{3,}\)', self.full_text):
            score += 12
        
        # Has URL (+15) - increased from 10 since having a link is very specific
        if "http" in self.full_text:
            score += 15
        
        # Has explicit answer/correct marker (+10)
        if any(x in self.full_text for x in ["(correct)", "(correct", "correct answer", "correct is", "should be"]):
            score += 10
        
        # Identifies incorrect/inconsistent information (+20)
        if any(x in self.full_text for x in ["incorrect", "inaccurate", "misleading", "misrepresent", "no such thing", "not", "alignment", "inconsistent"]):
            score += 20
        
        return min(score, 100)
    
    def _extract_context(self):
        """Extract available context from the issue"""
        context = {
            "has_url": "http" in self.full_text,
            "has_specific_module": any(x in self.full_text for x in ["unit", "module", "section", "assessment", "check your knowledge"]),
            "has_examples": bool(re.search(r'"[^"]{5,}"', self.full_text)) or bool(re.search(r'\([^)]{3,}\)', self.full_text)),
            "has_current_state": any(x in self.full_text for x in ["current", "says", "shows", "displays", "marked as", "is", "written", "described", "suggests"]),
            "has_desired_state": any(x in self.full_text for x in ["should be", "instead of", "should have", "should", "instead", "correct", "needs to be", "all code reviews", "require", "actually", "really"]),
            # Use cleaned body for length so template scaffolding doesn't inflate this
            "issue_length": len(self.cleaned_body.split()),
            "has_code": "```" in self.cleaned_body or bool(re.search(r'`[^`]+`', self.cleaned_body)),
            "has_screenshot": "screenshot" in self.full_text or "image" in self.full_text,
            "has_quiz_content": any(x in self.full_text for x in ["answer", "knowledge check", "question", "multiple choice", "correct", "quiz"]),
            # New: true when the body is essentially just the unfilled template
            "is_template_only": _is_effectively_empty(self.body),
        }
        return context
    
    @staticmethod
    def _looks_like_template_fragment(text):
        """Reject matches that are obviously checkbox/template scaffolding."""
        if not text:
            return True
        t = text.strip().lower()
        bad_substrings = [
            "add new content",
            "some other request",
            "update incorrect information",
            "fix a broken user experience",
            "[ ]", "[x]",
            "replace_with",
            "no response",
            "information ab",  # truncated "Information about..."
        ]
        return any(b in t for b in bad_substrings)

    def _extract_problem(self):
        """Extract the core problem from the issue"""
        # Try to extract "current -> desired" pattern
        problem = {
            "current": None,
            "desired": None,
            "location": None,
            "summary": None,
        }
        
        # Extract current state (what's wrong)
        # Pattern 1: "currently/now/says/shows..."
        current_match = re.search(
            r'(?:currently|now|says|shows|displays|marked as|written|suggests)(?:\s+[a-z]+)*\s+["\']?([^"\'.!?]{10,80})["\']?',
            self.full_text
        )
        if current_match and not self._looks_like_template_fragment(current_match.group(1)):
            problem["current"] = current_match.group(1).strip()
        
        # Pattern 2: Look for parenthetical marked items like "(Correct)" or "(Answer)"
        if not problem["current"]:
            paren_match = re.search(r'\(([^)]{5,50})\)\s*\n', self.full_text)
            if paren_match and not self._looks_like_template_fragment(paren_match.group(1)):
                problem["current"] = paren_match.group(1).strip()
        
        # Pattern 3: Look for natural language problem statements like "There is no such thing as..."
        if not problem["current"]:
            natural_problem = re.search(r'(There is (?:no|not)[^.!?]{15,80})', self.full_text)
            if natural_problem and not self._looks_like_template_fragment(natural_problem.group(1)):
                problem["current"] = natural_problem.group(1).strip()
        
        # Extract desired state (what should be)
        # Pattern 1: "should/should be/instead/needs to be..."
        desired_match = re.search(
            r'(?:should be|should|instead of|correct is|needs to be|correct|instead)(?:\s+[a-z]+)*\s+["\']?([^"\'.!?:]{8,80})["\']?',
            self.full_text
        )
        if desired_match and not self._looks_like_template_fragment(desired_match.group(1)):
            problem["desired"] = desired_match.group(1).strip()
        
        # Pattern 2: Look for explicit direction like "should be: None of them"
        explicit_desired = re.search(r'should be:\s*([^.\n]{5,80})', self.full_text)
        if explicit_desired and not self._looks_like_template_fragment(explicit_desired.group(1)):
            problem["desired"] = explicit_desired.group(1).strip()
        
        # Pattern 3: Look for fact statements like "all code reviews consume..."
        if not problem["desired"]:
            fact_match = re.search(r'(all (?:code reviews|PRU|[a-z]+s?) (?:consume|require)[^.!?]{8,80})', self.full_text)
            if fact_match and not self._looks_like_template_fragment(fact_match.group(1)):
                problem["desired"] = fact_match.group(1).strip()
        
        # Extract location
        location_keywords = ["in the", "on the", "under", "inside", "within", "at the", "in module", "check your", "knowledge check"]
        for keyword in location_keywords:
            match = re.search(rf'{keyword}\s+([^.!?,{{]{{3,60}})', self.full_text)
            if match and not self._looks_like_template_fragment(match.group(1)):
                problem["location"] = match.group(1).strip()
                break
        
        # Generate summary from title
        problem["summary"] = self.title.strip()
        
        return problem
    
    def _extract_proposed_fix(self):
        """Extract or infer the proposed fix"""
        fix = {
            "explicit": None,
            "inferred": None,
            "confidence": 0,
        }
        
        # Check for explicit fix suggestion
        explicit_match = re.search(
            r'(?:fix|change|update|replace|modify)(?:\s+(?:to|with))?\s+["\']?([^"\'.!?]{5,100})["\']?',
            self.full_text
        )
        if explicit_match:
            fix["explicit"] = explicit_match.group(1).strip()
            fix["confidence"] += 0.5
        
        # Infer fix if we have current/desired pattern
        if self.analysis.get("problem_statement"):
            problem = self.analysis["problem_statement"]
            if problem.get("current") and problem.get("desired"):
                fix["inferred"] = f"Replace '{problem['current']}' with '{problem['desired']}'"
                fix["confidence"] += 0.3
        
        fix["confidence"] = min(fix["confidence"], 1.0)
        return fix
    
    def _assess_actionability(self):
        """Assess if this issue is actionable (0-100)"""
        score = 0
        
        # Has issue type identified (+20)
        issue_types = self.analysis.get("issue_type", [])
        if issue_types:
            score += 20
        
        # Has context level (+20)
        context = self.analysis.get("context_level", {})
        if context.get("has_url"):
            score += 15
        if context.get("has_specific_module"):
            score += 15
        
        # Has specific problem described (+20)
        problem = self.analysis.get("problem_statement", {})
        if problem.get("current") or problem.get("desired"):
            score += 20
        
        # Has proposed fix (+20)
        fix = self.analysis.get("proposed_fix", {})
        if fix.get("explicit") or fix.get("inferred"):
            score += 20
        
        return min(score, 100)
    
    def _calculate_confidence(self):
        """Calculate confidence in auto-fix capability (0-100)"""
        score = 0
        context = self.analysis.get("context_level", {})
        
        # URL present (+30) - increased from 25 because having a link is very significant
        if context.get("has_url"):
            score += 30
        
        # Specific module (+20)
        if context.get("has_specific_module"):
            score += 20
        
        # Current AND desired states (+25)
        if context.get("has_current_state") and context.get("has_desired_state"):
            score += 25
        
        # Quiz/knowledge check content (+15) - these are highly actionable
        if context.get("has_quiz_content"):
            score += 15
        
        # Issue type not vague (+20) - increased from 15 to weight specific issue types more
        issue_types = self.analysis.get("issue_type", [])
        non_vague = [t for t in issue_types if t not in ["clarity_issue", "general_feedback"]]
        if non_vague:
            score += 20
        
        # Has good specificity (+15)
        if self.analysis.get("specificity_score", 0) > 50:
            score += 15
        
        return min(score, 100)


def intelligent_classify(issue):
    """
    Use intelligent analysis to classify issues
    Returns: (category, confidence_0_to_100, analysis)
    
    Classification Logic:
    - spam:          Template-only / empty / trivially short
    - auto_fix:      Has a clear, extractable current→desired change AND high signal
    - needs_human:   Has enough context but may need human review
    - needs_context: Missing critical information
    """
    title = issue.get("title", "")
    body = issue.get("body", "")
    
    # Quick spam filter: trivially short
    if len(f"{title}\n{body}".strip()) < 20:
        return "spam", 100, {}
    
    # Template-only spam filter: body is just unfilled MS Learn issue template
    if _is_effectively_empty(body):
        # Still build an analysis so downstream comment shows what we saw
        analyzer = IssueAnalyzer(title, body)
        analysis = analyzer.analyze()
        analysis["spam_reason"] = "template_only"
        return "spam", 100, analysis
    
    analyzer = IssueAnalyzer(title, body)
    analysis = analyzer.analyze()

    # A module selection is useful routing information, but it is not an
    # actionable request by itself. Close these as needs_context and invite
    # the author to reopen once the details field contains a concrete change.
    if _module_selected_without_update_details(body):
        return "needs_context", analysis["confidence"], analysis
    
    # All scores are already on a 0-100 scale
    confidence    = analysis["confidence"]
    actionability = analysis["actionability"]
    specificity   = analysis["specificity_score"]
    context       = analysis.get("context_level", {})
    problem       = analysis.get("problem_statement", {})
    has_url       = context.get("has_url", False)
    has_current   = bool(problem.get("current"))
    has_desired   = bool(problem.get("desired"))
    
    # AUTO-FIX: only when we have a concrete current AND desired to swap.
    # Without both, we cannot generate a safe patch, no matter how confident
    # the heuristics feel.
    #
    # Additionally, refuse auto_fix when the proposed "desired" looks more
    # like editorial commentary than a literal phrase to substitute:
    # heuristic = too long (>8 words) AND not quoted/parenthesized.
    desired_str = problem.get("desired") or ""
    desired_is_short_phrase = (
        len(desired_str.split()) <= 8
        or any(q in desired_str for q in ['"', "'"])
    )

    if (specificity >= 60 and confidence >= 70 and actionability >= 70
            and has_current and has_desired and desired_is_short_phrase):
        return "auto_fix", confidence, analysis
    
    # NEEDS_HUMAN: has URL + good specificity = enough info for a person
    if has_url and specificity >= 50:
        return "needs_human", confidence, analysis
    
    # NEEDS_HUMAN: medium confidence/actionability but decent specificity
    if (confidence >= 40 or actionability >= 40) and specificity >= 30:
        return "needs_human", confidence, analysis
    
    # NEEDS_CONTEXT: low specificity and low confidence
    if specificity < 30 and confidence < 50:
        return "needs_context", confidence, analysis
    
    # FALLBACK: if we have ANY URL, route to human
    if has_url:
        return "needs_human", confidence, analysis
    
    return "needs_context", confidence, analysis


def generate_context_aware_comment(analysis, classification):
    """
    Generate a helpful comment based on analysis
    """
    issue_types = analysis.get("issue_type", [])
    context = analysis.get("context_level", {})
    problem = analysis.get("problem_statement", {})
    fix = analysis.get("proposed_fix", {})
    
    if classification == "auto_fix":
        return f"""🧠 **Auto-triage Analysis:**

**Issue Type:** {', '.join(issue_types)}
**Specificity Score:** {analysis.get('specificity_score', 0)}/100
**Confidence:** {analysis.get('confidence', 0)}/100

I've identified this as an actionable issue:
- Location: {problem.get('location', 'Not specified')}
- Problem: {problem.get('current', 'Not clearly stated')}
- Should be: {problem.get('desired', 'Not clearly stated')}

Attempting to open a PR to fix this now! 🚀
(If no PR link appears in a follow-up comment, the auto-fix could not be applied — a human reviewer will take it from here.)"""
    
    elif classification == "needs_human":
        missing = []
        if not context.get("has_url"):
            missing.append("Direct MS Learn URL")
        if not context.get("has_specific_module"):
            missing.append("Specific module/unit reference")
        if not problem.get("current"):
            missing.append("Current state description")
        if not problem.get("desired"):
            missing.append("Desired state description")
        
        return f"""🚩 **Review Needed**

**Issue Type:** {', '.join(issue_types) or 'Not clearly categorized'}
**Specificity Score:** {analysis.get('specificity_score', 0)}/100

To help me proceed, please provide:
{chr(10).join(f'- {item}' for item in missing)}

Current info available:
- Module specific: {context.get('has_specific_module')}
- Has examples: {context.get('has_examples')}
- Issue length: {context.get('issue_length')} words"""
    
    else:  # needs_context
        return f"""❓ **Closed: More Specific Details Needed**

**Analysis:**
- Issue Type: {', '.join(issue_types) or 'Unclear'}
- Specificity Score: {analysis.get('specificity_score', 0)}/100

This issue does not contain a specific action we can take, so it has been closed for now. Please reopen it when you can provide:
1. **Direct link** to the MS Learn module or page
2. **Specific section** affected (unit, knowledge check, section, etc.)
3. **Current state:** What is shown/said now?
4. **Desired state:** What should it be?
5. **Examples:** Concrete code or text examples

This will help me automatically create a PR to fix it!"""


def generate_pr_description(issue, analysis):
    """
    Generate PR description based on issue analysis
    """
    problem = analysis.get("problem_statement", {})
    fix = analysis.get("proposed_fix", {})
    issue_types = analysis.get("issue_type", [])
    
    description = f"""## Fixes Issue #{issue['number']}

### Issue Type
{', '.join(issue_types)}

### Problem
{problem.get('current', 'Issue details from #' + str(issue['number']))}

### Solution
{fix.get('explicit') or fix.get('inferred') or 'Updated content to match learning objectives'}

### Context
- **Module:** {problem.get('location', 'See issue #' + str(issue['number']))}
- **Specificity Score:** {analysis['specificity_score']}/100

### Related Issue
Closes #{issue['number']}

---
*Auto-generated PR from intelligent issue analysis*
"""
    return description
