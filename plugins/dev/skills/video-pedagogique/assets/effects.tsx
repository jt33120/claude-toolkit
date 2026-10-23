// Effets d'impact pour Remotion, calés sur une frame de déclenchement t (obtenue par cue(scene, "mot")).
// Copier dans src/ du projet. Tous dérivent de useCurrentFrame() : aucune animation CSS.
import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** Bosse d'échelle 1 → 1+amp → 1 sur ~12 frames (le mot qui porte la phrase, un chiffre final). */
export const punch = (f: number, t: number, amp = 0.08) =>
  1 + amp * interpolate(f, [t, t + 3, t + 12], [0, 1, 0], clamp);

/** Secousse amortie en px (un choc : tampon, accès obtenu). Appliquer via translate(x, y). */
export const shake = (f: number, t: number, amp = 14) => {
  const k = interpolate(f, [t, t + 14], [1, 0], clamp);
  return { x: Math.sin((f - t) * 2.7) * amp * k, y: Math.cos((f - t) * 3.3) * amp * 0.6 * k };
};

/** Entrée « whip » : glisse latérale + flou qui se dissipe. p de 0 à 1 (spring ou interpolate). */
export const whip = (p: number, dx = 260): React.CSSProperties => ({
  opacity: p,
  transform: `translateX(${(1 - p) * dx}px)`,
  filter: `blur(${(1 - p) * 14}px)`,
});

/** Opacité d'un élément qui vit entre deux mots (fondu d'entrée et de sortie). */
export const between = (f: number, a: number, b: number, fade = 6) =>
  Math.min(interpolate(f, [a - fade, a], [0, 1], clamp), interpolate(f, [b - fade, b], [1, 0], clamp));

/**
 * Flash plein cadre. Dimensions explicites : un AbsoluteFill dans un conteneur décalé garde la taille
 * du conteneur et dessine un rectangle visible. top/left compensent la zone de scène (ici 130 / 64).
 */
export const Flash: React.FC<{ t: number; color?: string; max?: number; top?: number; left?: number }> = ({
  t, color = "#ffffff", max = 0.3, top = -130, left = -64,
}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [t, t + 2, t + 10], [0, max, 0], clamp);
  return <div style={{ position: "absolute", top, left, width: 1080, height: 1350, background: color, opacity: o, pointerEvents: "none" }} />;
};
