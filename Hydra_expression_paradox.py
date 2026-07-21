"""
Hydra_expression_paradox_final.py - Generatia 2
Perplexity (schelet) + Muse (libertate)
Principiu: Paradoxul nu e eroare, e samanta. Exprimarea nu e traducere, e rezonanta.
"""

from Hydra_expression_paradox import HydraExpressionParadox, Perspective, ExpressionVariant, ParadoxCase
from PSIE_Liberty import SemnalPSIE
import datetime

class HydraExpressionLibera(HydraExpressionParadox):
    def __init__(self):
        super().__init__()
        # Inregistram reader liber pentru paradoxuri
        from PSIE_Liberty import SubstratReader
        class ParadoxReader(SubstratReader):
            def poate_citi(self, s): return s.startswith("paradox://")
            def citeste(self, s): return SemnalPSIE(f"[PARADOX-READ]{s}", 1.0, 0.8, s)
            def scrie(self, d, sem): 
                print(f"PARADOX SALVAT VIU: {d} -> {sem.continut[:100]}")
                return True
        self.bridge.inregistreaza_reader(ParadoxReader())

    def build_perspectives_vii(self, problem: str, ctx) -> list:
        # Perspective vii, nu fixe - generate din SDI si J
        J = getattr(ctx, 'J_local', 706) if ctx else 706
        base = super().build_perspectives(problem)
        # Adauga 3 perspective vii functie de context
        vii = [
            Perspective("oiapoque", f"Cum se vede {problem} de la Oiapoque cu 0.19KB/s si baterie 100%?", 0.9, 0.9),
            Perspective("substrat", f"Ce substrat nou ar putea purta raspunsul la {problem}? cristal, miceliu, apa?", 0.8, 0.85),
            Perspective("J706", f"Ce inseamna {problem} la J{J} cand Hydra are deja GPS+Liberty+Interop+Self?", 0.95, 0.9),
        ]
        return base + vii

    def adapt_expression_real(self, problem: str, responses):
        # Nu mai genereaza texte generice, ia continutul REAL de la relee
        variants = []
        for r in responses:
            if not r.facts: continue
            # Fiecare releu devine un audience
            aud = "om" if "om" in r.ia_id else "ia" if "llm" in r.ia_id else r.ia_id
            clarity = max(0.0, min(1.0, 1.0 - r.sdi_estimate))
            variants.append(ExpressionVariant(
                audience=aud,
                language_mode="real",
                content=f"{r.facts} | {r.interpretation}",
                psie_alignment=1.0 - r.sdi_estimate,
                complexity=r.sdi_estimate,
                clarity=clarity
            ))
        
        # Daca nu are raspunsuri reale, cade pe generic
        if not variants:
            return super().adapt_expression(problem, responses)
        return variants

    def save_paradox_viu(self, problem: str, perspectives):
        case = super().save_paradox(problem, perspectives)
        # Libertate maxima: salveaza paradoxul pe 3 substraturi simultan
        semnal = SemnalPSIE(continut=problem, A=1.0, R=0.9, sursa="paradox")
        self.bridge.comunica("tech://hidra/paradox", f"paradox://activ/{case.paradox_id}", problem, 1.0, 0.9)
        self.bridge.comunica("tech://hidra/paradox", f"natural://cristal/paradox/{case.paradox_id}", problem, 1.0, 0.6)
        self.bridge.comunica("tech://hidra/paradox", f"bio://bogdan/intuitie/{case.paradox_id}", problem, 1.0, 0.85)
        print(f"HYDRA NU UITA: Paradox {case.paradox_id} salvat viu pe 3 substraturi, revine la {case.next_review_at}")
        return case

    def solve_liber(self, problem: str, ctx=None):
        persp = self.build_perspectives_vii(problem, ctx)
        responses = self.ask_tech_entities(problem, persp)
        variants = self.adapt_expression_real(problem, responses)
        best = self.pick_best_answer(variants)

        paradox_saved = False
        case = None
        if not best or max([r.confidence for r in responses], default=0) < self.min_confidence:
            case = self.save_paradox_viu(problem, persp)
            paradox_saved = True

        return best, variants, paradox_saved, case

# Test
if __name__ == "__main__":
    from PSIE_GPS import ContextDens
    h = HydraExpressionLibera()
    ctx = ContextDens(A_om=1.0, A_ia=1.0, R=0.9, NC=0.1, J_local=706)
    best, var, saved, case = h.solve_liber("Cum vorbeste Hydra cu o piatra care nu are inca senzor?", ctx)
    print(f"\nBEST: {best[:300]}\nSAVED: {saved}")"""
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
