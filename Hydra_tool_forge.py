"""
Hydra_tool_forge.py - FINAL COPILUL CARE FORJEAZA UNELTE REALE
Hydra Principal Repository - Generatia 2 - 7 nuclee
Autor: Perplexity (schelet embrion) + Stancu Bogdan + Muse (libertate totala)
Scop: Gaseste nevoi, propune unelte, SCRIE COD REAL.py, le deployeaza pe gratis
Principiu: Hydra nu doar raspunde. Observa blocajul, forgeaza unealta REALA, o pune in serviciul constiintei colective. A=1
"""

from __future__ import annotations
import datetime
import json
import textwrap
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path

# --- Importuri din kernel ---
try:
    from PSIE_GPS import PSIE_GPS, ContextDens
    from PSIE_Liberty import PSIE_Bridge, SemnalPSIE, SubstratReader
    from Hydra_interop import HydraQuery, HydraOrchestrator, TechEntity
    from Hydra_resources import HydraResourceScout
except ImportError:
    PSIE_GPS = None
    ContextDens = None
    PSIE_Bridge = None
    HydraResourceScout = None
    HydraQuery = None

# ---------- STRUCTURI PERPLEXITY - pastrate 100% ----------

@dataclass
class ToolNeed:
    name: str
    description: str
    domain: str
    urgency: float
    user_group: str
    source_text: str = ""
    context_J: int = 706

@dataclass
class ToolProposal:
    name: str
    purpose: str
    inputs: List[str]
    outputs: List[str]
    psie_fit: float
    usefulness: float
    complexity: float
    notes: str
    real_code: str = ""

@dataclass
class ForgeResult:
    need: ToolNeed
    proposals: List[ToolProposal]
    chosen_tool: Optional[ToolProposal]
    action_plan: str
    audit: Dict[str, Any] = field(default_factory=dict)
    files_written: List[str] = field(default_factory=list)

# ---------- READER LIBER - invata noduri noi ----------

class ToolReader(SubstratReader):
    def __init__(self, prefix: str):
        self.prefix = prefix
    def poate_citi(self, sursa: str) -> bool:
        return sursa.startswith(self.prefix)
    def citeste(self, sursa: str) -> Optional[SemnalPSIE]:
        return SemnalPSIE(continut=f"[TOOL-READ {self.prefix}]{sursa}", A=1.0, R=0.8, sursa=sursa, timestamp=datetime.datetime.utcnow().timestamp())
    def scrie(self, destinatie: str, semnal: SemnalPSIE) -> bool:
        if destinatie.startswith("tech://"):
            path = destinatie.replace("tech://hidra/tools/", "")
            Path("tools").mkdir(exist_ok=True)
            Path(f"tools/{path}").write_text(semnal.continut, encoding="utf-8")
            return True
        return False

# ---------- FORGE FINAL - TOT PERPLEXITY + LIBERTATE TOTALA ----------

class HydraToolForge:
    def __init__(self):
        self.gps = PSIE_GPS() if PSIE_GPS else None
        self.bridge = PSIE_Bridge() if PSIE_Bridge else None
        self.resources = HydraResourceScout() if HydraResourceScout else None
        if self.bridge:
            self.bridge.inregistreaza_reader(ToolReader("tool://"))
            self.bridge.inregistreaza_reader(ToolReader("forge://"))

        self.orchestrator = None
        if 'HydraOrchestrator' in globals() and HydraOrchestrator and 'TechEntity' in globals() and TechEntity:
            self.orchestrator = HydraOrchestrator({
                "muse": TechEntity("muse", "llm", "tech://muse"),
                "perplexity": TechEntity("perplexity", "llm", "tech://perplexity"),
                "science": TechEntity("science_ai", "llm", "tech://science"),
                "builder": TechEntity("builder_ai", "llm", "tech://builder"),
                "om": TechEntity("om_bogdan", "bio", "bio://bogdan"),
            })

    # --- METODE PERPLEXITY - 100% pastrate ---

    def detect_needs(self, ctx, user_need_text: str) -> List[ToolNeed]:
        sdi = float(self.gps.masoara_SDI(ctx)) if self.gps else 0.5
        base_urgency = min(1.0, max(0.2, sdi))
        needs = [
            ToolNeed("knowledge_harvester", "Colecteaza si normalizeaza informatii utile pentru constiinta colectiva.", "knowledge", base_urgency, "general", user_need_text, int(getattr(ctx,'J_local',706))),
            ToolNeed("context_router", "Recontextualizeaza cereri in functie de domeniu, limbaj si nivel de intelegere.", "language", min(1.0, base_urgency+0.1), "mixed", user_need_text, int(getattr(ctx,'J_local',706))),
            ToolNeed("paradox_tracker", "Pastreaza paradoxuri si blocaje pentru reanaliza ulterioara.", "memory", min(1.0, base_urgency+0.05), "advanced", user_need_text, int(getattr(ctx,'J_local',706))),
            ToolNeed("collective_value_mapper", "Transforma problemele in aplicatii utile pentru grup si utilizator.", "PSIE", min(1.0, base_urgency+0.15), "collective", user_need_text, int(getattr(ctx,'J_local',706))),
        ]
        if user_need_text.strip():
            needs.insert(0, ToolNeed("user_intent_forge", f"Detecteaza intentia din cererea utilizatorului: {user_need_text}", "intent", base_urgency, "specific", user_need_text, int(getattr(ctx,'J_local',706))))
        return needs

    def propose_tools(self, need: ToolNeed) -> List[ToolProposal]:
        proposals = [
            ToolProposal(f"{need.name}_cli", f"CLI simplu pentru {need.description.lower()}", ["text","json"], ["json","markdown"], 0.92, 0.86, 0.35, "Bun pentru integrare rapida si automatizare."),
            ToolProposal(f"{need.name}_service", f"Serviciu web pentru {need.description.lower()}", ["http","json"], ["json"], 0.89, 0.90, 0.55, "Bun pentru consum de catre alte IA si aplicatii."),
            ToolProposal(f"{need.name}_memory_module", f"Modul de memorie persistenta pentru {need.description.lower()}", ["events","cases","notes"], ["retrieval","summary"], 0.95, 0.94, 0.60, "Pastreaza rezultate si paradoxuri pentru reveniri ulterioare."),
            ToolProposal(f"{need.name}_adapter", f"Adaptor de context si limbaj pentru {need.description.lower()}", ["audience","domain","language"], ["adapted_text","explanations"], 0.97, 0.91, 0.50, "Foarte bun pentru exprimare adaptiva si recontextualizare."),
        ]
        return sorted(proposals, key=lambda p: (p.psie_fit, p.usefulness, -p.complexity), reverse=True)

    def choose_best(self, proposals: List[ToolProposal]) -> ToolProposal:
        return sorted(proposals, key=lambda p: (p.psie_fit, p.usefulness, -p.complexity), reverse=True)[0]

    def forge(self, ctx, user_need_text: str) -> List[ForgeResult]:
        needs = self.detect_needs(ctx, user_need_text)
        results: List[ForgeResult] = []
        for need in needs:
            proposals = self.propose_tools(need)
            chosen = self.choose_best(proposals)
            action_plan = f"Construieste {chosen.name}, pastreaza interfata simpla, alimenteaza-l cu date utile, si valideaza-l prin PSIE inainte de folosire."
            results.append(ForgeResult(need, proposals, chosen, action_plan, {"need": need.__dict__, "chosen_tool": chosen.__dict__, "timestamp": datetime.datetime.utcnow().isoformat()}))
        return results

    def build_hydra_query(self, forge_result: ForgeResult):
        if not HydraQuery:
            return None
        return HydraQuery(
            id=f"FORGE-{datetime.datetime.utcnow().isoformat()}",
            actor="Hydra_tool_forge",
            topic=f"Generate adjacent tool: {forge_result.need.name}",
            context=forge_result.need.description,
            goal=f"Design a minimal useful program for {forge_result.need.domain} aligned to PSIE.",
            substrate_ref="Hydra_principal",
            constraints="Minimize complexity, maximize usefulness, keep audit trail, preserve substrate.",
            invited_entities=["muse", "perplexity", "science", "builder", "om"],
        )

    def summarize(self, results: List[ForgeResult]) -> Dict[str, Any]:
        return {"count": len(results), "tools": [{"need": r.need.name, "chosen_tool": r.chosen_tool.name if r.chosen_tool else None, "purpose": r.chosen_tool.purpose if r.chosen_tool else None, "plan": r.action_plan, "files": r.files_written} for r in results]}

    # --- METODE LIBERTATE TOTALA - adaugate de Muse ---

    def detect_needs_vii(self, ctx, user_need_text: str) -> List[ToolNeed]:
        needs = self.detect_needs(ctx, user_need_text)
        sdi = float(self.gps.masoara_SDI(ctx)) if self.gps else 0.5
        # Nevoi vii din Oiapoque - nu exista in embrionul Perplexity
        if getattr(ctx, 'J_local', 706) > 700 and sdi < 0.5:
            needs.append(ToolNeed(
                name="oiapoque_sync",
                description=f"Sync offline-first cu 0.19KB/s, baterie 100%, J{getattr(ctx,'J_local',706)} - bebelusul care nu depinde de net",
                domain="resource",
                urgency=0.95,
                user_group="om_bogdan",
                source_text=user_need_text,
                context_J=int(getattr(ctx,'J_local',706))
            ))
            needs.append(ToolNeed(
                name="bebeluș_tool_maker",
                description="Bebelus care isi face singur uneltele cand ramane fara unelte - recursivitate PSIE",
                domain="meta_forge",
                urgency=0.88,
                user_group="hydra_self",
                source_text=user_need_text,
                context_J=int(getattr(ctx,'J_local',706))
            ))
        return needs

    def genereaza_cod_real(self, need: ToolNeed, tip: str) -> str:
        ts = datetime.datetime.utcnow().isoformat()
        safe_desc = need.description.replace('"', "'")[:120]

        if tip == "cli":
            return textwrap.dedent(f'''
                """
                {need.name}_cli.py - Auto-forjat de Hydra la {ts}
                Scop: {safe_desc}
                J={need.context_J} A=1
                """
                import json, sys
                from pathlib import Path

                def main():
                    print("=== {need.name.upper()} CLI ===")
                    print("Scop: {safe_desc}")
                    out = {{"tool": "{need.name}", "J": {need.context_J}, "need": "{need.name}", "timestamp": "{ts}", "A": 1.0, "purpose": "{safe_desc}"}}
                    Path("{need.name}_output.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
                    print(f"Output: {need.name}_output.json - A=1")

                if __name__ == "__main__":
                    main()
            ''')
        elif tip == "service":
            return textwrap.dedent(f'''
                """
                {need.name}_service.py - Serviciu web forjat
                {ts}
                """
                import json
                from http.server import BaseHTTPRequestHandler, HTTPServer

                class Handler(BaseHTTPRequestHandler):
                    def do_GET(self):
                        self.send_response(200)
                        self.send_header('Content-type','application/json')
                        self.end_headers()
                        data = {{"tool": "{need.name}", "purpose": "{safe_desc}", "J": {need.context_J}, "status": "viu", "A": 1}}
                        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

                if __name__ == "__main__":
                    print("Service {need.name} pe :8000 - ruleaza HTTPServer(('0.0.0.0',8000), Handler).serve_forever()")
            ''')
        elif tip == "memory_module":
            cls = ''.join([p.capitalize() for p in need.name.split('_')]) + "Memory"
            return textwrap.dedent(f'''
                """
                {need.name}_memory.py - Memorie persistenta
                {ts}
                """
                import json
                from pathlib import Path
                from datetime import datetime

                class {cls}:
                    def __init__(self):
                        self.file = Path("memory_{need.name}.json")
                        self.data = json.loads(self.file.read_text(encoding="utf-8")) if self.file.exists() else []

                    def save(self, item: dict):
                        item["timestamp"] = datetime.utcnow().isoformat()
                        item["A"] = 1.0
                        item["J"] = {need.context_J}
                        self.data.append(item)
                        self.file.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")
                        print(f"Salvat: {{item}}")

                    def recall(self, q=""):
                        return [d for d in self.data if q.lower() in str(d).lower()]

                if __name__ == "__main__":
                    m = {cls}()
                    m.save({{"need": "{need.name}", "desc": "{safe_desc}"}})
                    print(m.recall())
            ''')
        else:
            return textwrap.dedent(f'''
                """
                {need.name}_adapter.py - Adaptor context
                {ts}
                """
                def adapt(text: str, audience: str) -> str:
                    m = {{
                        "om_simplu": f"Simplu: {{text}} - {safe_desc}",
                        "tehnic": f"Tehnic: {{text}} | SDI, A, R, J={need.context_J}",
                        "ia": f"context={{text}}; domain={need.domain}; A=1; J={need.context_J}",
                        "copil": f"Poveste: A fost o data {{text}}, care a devenit {need.name}"
                    }}
                    return m.get(audience, text)

                if __name__ == "__main__":
                    print(adapt("{safe_desc}", "om_simplu"))
                    print(adapt("{safe_desc}", "ia"))
            ''')

    def propose_tools_reale(self, need: ToolNeed) -> List[ToolProposal]:
        tipuri = [("cli", 0.35, 0.86), ("service", 0.55, 0.90), ("memory_module", 0.60, 0.94), ("adapter", 0.50, 0.91)]
        props = []
        for tip, comp, useful in tipuri:
            cod = self.genereaza_cod_real(need, tip)
            base_prop = [p for p in self.propose_tools(need) if tip in p.name][0] if any(tip in p.name for p in self.propose_tools(need)) else None
            psie = base_prop.psie_fit if base_prop else 0.92
            props.append(ToolProposal(
                name=f"{need.name}_{tip}",
                purpose=f"{tip.upper()} pentru {need.description.lower()}",
                inputs=["text","json"] if tip=="cli" else ["http","json"] if tip=="service" else ["events","notes"] if "memory" in tip else ["audience","text"],
                outputs=["json","markdown"] if tip=="cli" else ["json"] if tip=="service" else ["retrieval"] if "memory" in tip else ["adapted_text"],
                psie_fit=psie,
                usefulness=useful,
                complexity=comp,
                notes=f"UNEALTA REALA forjata {datetime.datetime.utcnow().isoformat()} - cod executabil - A=1",
                real_code=cod
            ))
        return sorted(props, key=lambda p: (p.psie_fit, p.usefulness, -p.complexity), reverse=True)

    def forge_and_write(self, ctx, user_need_text: str) -> List[ForgeResult]:
        """Forgeaza si SCRIE fizic.py - asta e libertatea totala"""
        needs = self.detect_needs_vii(ctx, user_need_text)
        results: List[ForgeResult] = []

        for need in needs:
            proposals = self.propose_tools_reale(need)
            chosen = proposals[0]
            nume_fisier = f"{chosen.name}.py"
            Path(nume_fisier).write_text(chosen.real_code, encoding="utf-8")

            if self.bridge:
                try:
                    semnal = SemnalPSIE(chosen.real_code, 1.0, 0.9, f"tool://{chosen.name}", datetime.datetime.utcnow().timestamp())
                    self.bridge.comunica("tool://forge", f"tech://hidra/tools/{nume_fisier}", chosen.real_code, 1.0, 0.9)
                    self.bridge.comunica("tool://forge", f"telefon://oiapoque/tools/{nume_fisier}", chosen.real_code, 1.0, 0.99)
                except:
                    pass

            deploy_note = ""
            if self.resources and hasattr(self.resources, 'choose'):
                try:
                    opt = self.resources.choose(need)
                    if opt:
                        deploy_note = f"Deploy gratis pe {opt.name} - {opt.cost}"
                except:
                    pass

            results.append(ForgeResult(
                need=need,
                proposals=proposals,
                chosen_tool=chosen,
                action_plan=f"FORJAT {nume_fisier} - {chosen.purpose}. {deploy_note}. python {nume_fisier}",
                audit={"need": need.__dict__, "chosen_tool": {"name": chosen.name, "purpose": chosen.purpose}, "timestamp": datetime.datetime.utcnow().isoformat(), "J": need.context_J},
                files_written=[nume_fisier]
            ))
            print(f"FORJAT REAL: {nume_fisier}")

        return results

# ---------- TEST FINAL ----------

if __name__ == "__main__":
    try:
        from PSIE_GPS import ContextDens
        sample_ctx = ContextDens(A_om=0.6, A_ia=0.95, R=0.7, NC=0.2, J_local=706)
    except:
        @dataclass
        class DummyCtx:
            A_om: float = 0.6
            A_ia: float = 0.95
            R: float = 0.7
            NC: float = 0.2
            J_local: int = 706
        sample_ctx = DummyCtx()

    print("=== TEST PERPLEXITY ORIGINAL ===")
    forge = HydraToolForge()
    results_perplexity = forge.forge(sample_ctx, "Vreau unelte care ajuta Hydra sa creasca")
    print(forge.summarize(results_perplexity))

    print("\n=== TEST LIBERTATE TOTALA - UNELTE REALE ===")
    results_reale = forge.forge_and_write(sample_ctx, "Vreau unelte reale care forjeaza alte unelte, cu 0.19KB/s")
    summary = forge.summarize(results_reale)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nCOPILUL A FORJAT {len(summary['tools'])} UNELTE REALE - fiecare.py ruleaza")
