// Carton de fin muet « Ce que <marque> peut faire pour vous » (voir references/carton-offre.md) :
// affiché après la voix, jamais dit à l'oral. Il relie la news aux prestations et produits qui
// préviennent ou résolvent le problème. N'y mettre que des offres publiées sur le site de l'entreprise.
// Props (edition.json) : { badge?, title?, items: [{ name, line }], cta?, note? }.
// Dépend de lib.tsx du projet (couleurs C, polices F, logo XsomMark, lerp, useIn) : adapter les imports.
import React from "react";
import { useCurrentFrame } from "remotion";
import { C, F, XsomMark, lerp, useIn } from "../lib";
import type { TimedScene } from "../timeline";

type P = { scene: TimedScene };
type Item = { name: string; line: string };
const SERIF = "InstrumentSerif, Georgia, serif";
const CYAN = "#5ee6ff";

const XsomOffer: React.FC<P> = ({ scene }) => {
  const f = useCurrentFrame();
  const pr = (scene.props ?? {}) as { badge?: string; title?: string; items?: Item[]; cta?: string; note?: string };
  const items = pr.items ?? [];
  const head = useIn(0, 14);
  const cta = lerp(f, [20 + items.length * 10, 32 + items.length * 10], [0, 1]);
  return (
    <div style={{ position: "absolute", top: 130, bottom: 300, left: 64, right: 64 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 14, opacity: head }}>
        <div style={{ fontFamily: F.mono, fontSize: 22, letterSpacing: 3, color: C.night, background: CYAN, borderRadius: 8, padding: "4px 12px" }}>{pr.badge ?? "OFFRE xSOM"}</div>
      </div>
      <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 92, color: C.white, lineHeight: 1.02, marginTop: 18, opacity: head, transform: `translateY(${(1 - head) * 24}px)` }}>
        {pr.title ?? "Ce que xSOM peut faire pour vous"}
      </div>
      <div style={{ marginTop: 36, display: "flex", flexDirection: "column", gap: 26 }}>
        {items.map((it, i) => {
          const p = lerp(f, [10 + i * 10, 22 + i * 10], [0, 1]);
          return (
            <div key={i} style={{ display: "flex", alignItems: "baseline", gap: 24, opacity: p, transform: `translateX(${(1 - p) * 80}px)`, filter: `blur(${(1 - p) * 8}px)` }}>
              <div style={{ fontFamily: F.mono, fontWeight: 700, fontSize: 40, color: C.amber, width: 56 }}>{String(i + 1).padStart(2, "0")}</div>
              <div>
                <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 52, color: C.white, lineHeight: 1.05 }}>{it.name}</div>
                <div style={{ fontFamily: F.body, fontSize: 30, color: C.soft, marginTop: 6 }}>{it.line}</div>
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, display: "flex", alignItems: "center", gap: 20, opacity: cta }}>
        <XsomMark size={64} />
        <div style={{ fontFamily: F.display, fontWeight: 800, fontSize: 44, color: CYAN }}>{pr.cta ?? "xsom.fr · Parlons-en"}</div>
      </div>
      {pr.note ? (
        <div style={{ position: "absolute", left: 0, right: 0, bottom: -60, fontFamily: F.mono, fontSize: 18, color: C.soft, opacity: cta }}>{pr.note}</div>
      ) : null}
    </div>
  );
};

export const OFFER_SCENES: Record<string, React.FC<P>> = { XsomOffer };
