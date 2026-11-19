#!/usr/bin/env python3
"""Texture d'écran cathodique (CRT) et glitchs, ajoutés APRÈS le rendu avec ffmpeg.

Dans Chrome, les `filter` CSS et `mix-blend-mode` produisent des images corrompues sur les rendus
longs : la texture se fait donc ici, image par image, de façon déterministe.

usage : python3 crt.py in.mp4 out.mp4 [--glitch 5.0:0.3 ...] [--soft] [--micro]
  --glitch T:D   glitch fort à T secondes pendant D secondes (bandes décalées, couleurs déchirées)
                 → le placer sur le mot qui le justifie (erreur, danger) : 2 à 5 par minute au plus
  --soft         texture discrète (cours) : lignes et grain plus légers
  --micro        micro-glitchs de 2 images toutes les 7 à 11 s (style « l'écran vit »)
Lancer deglitch AVANT ce passage : les glitchs voulus seraient sinon pris pour des images corrompues.
Effets constants : halo, léger décalage des couleurs, lignes de balayage, barre lumineuse qui défile,
grain, vignettage, bombé de l'écran, scintillement. Image ré-encodée en CRF 19, son copié.
"""
import argparse, os, subprocess, tempfile
import numpy as np


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--glitch', action='append', default=[])
    ap.add_argument('--soft', action='store_true'); ap.add_argument('--micro', action='store_true')
    a = ap.parse_args()
    total = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.src]).decode().strip().strip(','))
    win = [(float(g.split(':')[0]), float(g.split(':')[1])) for g in a.glitch]
    if a.micro:
        rng = np.random.default_rng(11); t = 6.0
        while t < total - 2:
            if all(abs(t - s) > 2 for s, _ in win): win.append((t, 0.067))
            t += rng.uniform(7, 11)
    win.sort()
    scan_a, noise = ('38', '4') if a.soft else ('70', '7')
    tmp = tempfile.mkdtemp(); scan, bar = f'{tmp}/scan.png', f'{tmp}/bar.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', "color=c=black:s=1920x1080,format=rgba,geq=r=0:g=0:b=0:a='if(lt(mod(Y\\,4)\\,2)\\," + scan_a + "\\,0)'", '-frames:v', '1', scan], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', "color=c=white:s=1920x220,format=rgba,geq=r=255:g=255:b=255:a='10*sin(PI*Y/220)'", '-frames:v', '1', bar], check=True)
    rng = np.random.default_rng(5); parts = []; cur = 'base'
    nb = 2 * len(win)
    parts.append(f'[0:v]scale=1920:1080,format=yuv420p,split={nb + 1}[base]' + ''.join(f'[c{k}]' for k in range(nb)))
    for k, (s, d) in enumerate(win):
        for j in range(2):
            i = 2 * k + j; h = int(rng.uniform(40, 180)); y = int(rng.uniform(80, 1080 - h - 80)); dx = int(rng.uniform(-90, 90)) or 40
            parts.append(f'[c{i}]crop=1920:{h}:0:{y}[b{i}]')
            parts.append(f"[{cur}][b{i}]overlay=x={dx}:y={y}:enable='between(t,{s:.3f},{s + d:.3f})'[o{i}]"); cur = f'o{i}'
    en = '+'.join(f'between(t,{s:.3f},{s + d:.3f})' for s, d in win) or '0'
    parts += [f"[{cur}]rgbashift=rh=-16:bh=16:gv=4:enable='{en}'[g1]",
              '[g1]split[m][h];[h]gblur=sigma=14[hb];[m][hb]blend=all_mode=screen:all_opacity=0.22[bl]',
              '[bl]rgbashift=rh=-2:bh=2[ca]', '[ca][1:v]overlay=0:0:shortest=1[sl]',
              "[sl][2:v]overlay=x=0:y='mod(t*170\\,1300)-220'[rb]",
              f"[rb]noise=alls={noise}:allf=t,vignette=angle=PI/4.2,lenscorrection=k1=-0.03:k2=-0.01,eq=brightness='0.012*sin(2*PI*t*7)':eval=frame,format=yuv420p[v]"]
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.src, '-loop', '1', '-i', scan, '-loop', '1', '-i', bar, '-filter_complex', ';'.join(parts),
                    '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-c:a', 'copy', '-movflags', '+faststart', '-shortest', a.dst], check=True)
    print(f'{a.dst} : CRT{" discret" if a.soft else ""}, {len(win)} glitch(s)')


main()
