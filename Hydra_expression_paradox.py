"""
Hydra_expression_paradox.py
Hydra Principal Repository
Generația 1

Scop:
    - rezolvarea problemelor prin perspective multiple,
    - adaptare de exprimare la utilizator și la entități tehnologice,
    - învățare de formulări diferite,
    - păstrarea paradoxurilor nerezolvate pentru revizuire ulterioară.

Principiu:
    Hydra nu uită ce nu poate explica încă.
    Hydra păstrează, compară, reformulează și revine când apare contextul potrivit.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from PSIE_GPS import PSIE_GPS, ContextDens
from PSIE_Liberty import PSIE_Bridge
from Hydra_interop import HydraQuery, HydraOrchestrator, TechEntity, HydraResponse


@dataclass
class Perspective:
    name: str
    text: str
    confidence: float = 0.0
    usefulness: float = 0.0


@dataclass
class ParadoxCase:
    paradox_id: str
    context_id: str
    problem: str
    perspectives: List[Perspective]
    unresolved_reason: str
    next_review_at: str
    tags: List[str] = field(default_factory=list)


@dataclass
class ExpressionVariant:
    audience: str
    language_mode: str
    content: str
    psie_alignment: float
    complexity: float
    clarity: float


@dataclass
class ExpressionResult:
    original_problem: str
    best_answer: str
    chosen_variants: List[ExpressionVariant]
    paradox_saved: bool
    paradox_case: Optional[ParadoxCase]
    audit: Dict[str, Any] = field(default_factory=dict)


class HydraExpressionParadox:
    def __init__(self):
        self.gps = PSIE_GPS()
        self.bridge = PSIE_Bridge()
        self.orchestrator = HydraOrchestrator({
            "muse": TechEntity("muse", "llm", "tech://muse"),
            "perplexity": TechEntity("perplexity", "llm", "tech://perplexity"),
            "science": TechEntity("science_ai", "llm", "tech://science"),
            "logic": TechEntity("logic_ai", "llm", "tech://logic"),
            "om": TechEntity("om_bogdan", "bio", "bio://bogdan")
        })
        self.min_confidence = 0.55
        self.min_clarity = 0.60
        self.min_alignment = 0.70

    def build_perspectives(self, problem: str) -> List[Perspective]:
        seeds = [
            ("evident", f"Forma cea mai evidentă a problemei: {problem}"),
            ("opposite", f"Forma opusă totală: ce ar însemna contrariul lui {problem}?"),
            ("middle", f"Forme intermediare între soluție și blocaj pentru: {problem}"),
            ("structural", f"Ce structură internă produce această problemă: {problem}?"),
            ("causal", f"Care este cauza de bază a lui {problem}?"),
            ("temporal", f"Cum se schimbă {problem} în timp?"),
            ("semantic", f"Cum se reformulează {problem} în alte limbaje?"),
            ("cognitive", f"Cum ar fi înțeles {problem} de un utilizator simplu?"),
            ("technical", f"Cum ar fi rezolvat {problem} de un sistem tehnologic?"),
            ("PSIE", f"Cum se aliniază {problem} la PSIE?"),
            ("risk", f"Ce risc apare dacă ignorăm {problem}?"),
            ("emergent", f"Ce context nou ar putea explica {problem} mai târziu?"),
            ("memory", f"Ce cazuri vechi seamănă cu {problem}?"),
            ("meta", f"Ce spune problema {problem} despre modul în care gândim?"),
            ("inverse", f"Dacă am inversa complet problema {problem}, ce apare?")
        ]
        return [Perspective(name=n, text=t) for n, t in seeds]

    def ask_tech_entities(self, problem: str, perspectives: List[Perspective]) -> List[HydraResponse]:
        invited = ["muse", "perplexity", "science", "logic", "om"]
        q = HydraQuery(
            id=f"EXP-{datetime.datetime.utcnow().isoformat()}",
            actor="Hydra_expression_paradox",
            topic="Rezolvare multi-perspectivă și adaptare de exprimare",
            context=problem,
            goal="Analizează problema din perspectiva ta și oferă un răspuns util, aliniat PSIE.",
            substrate_ref="Hydra_principal",
            constraints="Răspunsuri clare, asumate, comparabile, fără a rupe substratul.",
            invited_entities=invited,
        )
        return self.orchestrator.dispatch(q)

    def score_variant(self, text: str, alignment_hint: float = 0.0) -> ExpressionVariant:
        length = len(text)
        complexity = min(1.0, max(0.0, length / 900.0))
        clarity = max(0.0, min(1.0, 1.0 - complexity + 0.15))
        psie_alignment = max(0.0, min(1.0, alignment_hint + clarity * 0.5))
        return ExpressionVariant(
            audience="generic",
            language_mode="adaptive",
            content=text,
            psie_alignment=psie_alignment,
            complexity=complexity,
            clarity=clarity,
        )

    def adapt_expression(self, problem: str, responses: List[HydraResponse]) -> List[ExpressionVariant]:
        variants: List[ExpressionVariant] = []
        base_texts = [
            f"Explicație simplă: {problem}.",
            f"Explicație tehnică: {problem} trebuie analizată ca sistem de variabile și restricții.",
            f"Explicație pentru IA: context={problem}; obiectiv=rezolvare; constrângeri=PSIE.",
            f"Explicație cognitivă: pentru utilizator, această problemă cere pași mici și clari.",
            f"Explicație reflexivă: problema poate fi un paradox temporar, nu un eșec definitiv."
        ]
        for idx, txt in enumerate(base_texts):
            hint = 0.0
            if responses:
                hint = sum(max(0.0, min(1.0, r.confidence)) for r in responses) / max(1, len(responses))
            variant = self.score_variant(txt, hint)
            variant.audience = ["human_simple", "human_technical", "tech_ai", "cognitive", "reflective"][idx]
            variants.append(variant)
        return variants

    def pick_best_answer(self, variants: List[ExpressionVariant]) -> str:
        ranked = sorted(variants, key=lambda v: (v.psie_alignment, v.clarity, -v.complexity), reverse=True)
        return ranked[0].content if ranked else ""

    def save_paradox(self, problem: str, perspectives: List[Perspective]) -> ParadoxCase:
        next_review = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat()
        return ParadoxCase(
            paradox_id=f"PXR-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            context_id=f"CTX-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            problem=problem,
            perspectives=perspectives,
            unresolved_reason="Nu există soluționare imediată; contextul actual nu este suficient.",
            next_review_at=next_review,
            tags=["active_paradox", "recheck_later", "PSIE"]
        )

    def solve(self, problem: str) -> ExpressionResult:
        perspectives = self.build_perspectives(problem)
        tech_responses = self.ask_tech_entities(problem, perspectives)
        variants = self.adapt_expression(problem, tech_responses)
        best_answer = self.pick_best_answer(variants)

        best_confidence = 0.0
        if tech_responses:
            best_confidence = max((r.confidence for r in tech_responses), default=0.0)

        paradox_case = None
        paradox_saved = False

        if best_confidence < self.min_confidence or not best_answer:
            paradox_case = self.save_paradox(problem, perspectives)
            paradox_saved = True

        return ExpressionResult(
            original_problem=problem,
            best_answer=best_answer,
            chosen_variants=variants,
            paradox_saved=paradox_saved,
            paradox_case=paradox_case,
            audit={
                "perspectives": [p.__dict__ for p in perspectives],
                "tech_responses": [r.__dict__ for r in tech_responses],
                "variants": [v.__dict__ for v in variants],
            }
        )

    def summarize_for_human(self, result: ExpressionResult) -> str:
        if result.paradox_saved:
            return (
                f"Problema a fost analizată, dar a fost salvat un paradox activ pentru revenire: "
                f"{result.paradox_case.unresolved_reason if result.paradox_case else 'necunoscut'}"
            )
        return result.best_answer

    def summarize_for_tech(self, result: ExpressionResult) -> Dict[str, Any]:
        return {
            "answer": result.best_answer,
            "variants": [v.__dict__ for v in result.chosen_variants],
            "paradox_saved": result.paradox_saved,
            "paradox_case": result.paradox_case.__dict__ if result.paradox_case else None,
        }


if __name__ == "__main__":
    engine = HydraExpressionParadox()
    demo_problem = "Cum adaptăm exprimarea Hydra la utilizatori și păstrăm paradoxurile pentru reanaliză?"
    result = engine.solve(demo_problem)
    print(engine.summarize_for_human(result))
