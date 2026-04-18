from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
#  AntoTarot  –  "Iubire și Adevăr"
#  Render:  manim -pqh anto_tarot_intro.py AntoTarotIntro
# ─────────────────────────────────────────────────────────────────────────────

class AntoTarotIntro(Scene):
    def construct(self):
        # ── Palette ──────────────────────────────────────────────────────────
        BG          = "#0D0820"   # near-black violet
        GOLD        = "#FFD700"
        PALE_GOLD   = "#FFF5B0"
        ROSE        = "#FF85A1"
        LILAC       = "#C9A0FF"
        TEAL        = "#7FFFD4"
        STAR_COL    = "#E8DDFF"
        DEEP_ROSE   = "#C0355A"
        SILVER      = "#D0C8FF"

        self.camera.background_color = BG
        rng = np.random.default_rng(7)

        # ════════════════════════════════════════════════════════════════════
        # LAYER 0 – BACKGROUND STARS (two sizes / opacities)
        # ════════════════════════════════════════════════════════════════════
        def make_stars(n, r_lo, r_hi, op_lo, op_hi):
            return VGroup(*[
                Dot(
                    point=[rng.uniform(-7.5, 7.5), rng.uniform(-4.3, 4.3), 0],
                    radius=rng.uniform(r_lo, r_hi),
                    color=STAR_COL,
                ).set_opacity(rng.uniform(op_lo, op_hi))
                for _ in range(n)
            ])

        stars_bg = make_stars(160, 0.012, 0.035, 0.15, 0.55)
        stars_fg = make_stars(40,  0.04,  0.07,  0.5,  0.95)

        # ════════════════════════════════════════════════════════════════════
        # LAYER 1 – OUTER ZODIAC WHEEL
        # ════════════════════════════════════════════════════════════════════
        ZODIAC_SYMBOLS = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]
        R_WHEEL = 3.45

        wheel_ring_outer = Circle(radius=R_WHEEL + 0.22, color=GOLD, stroke_width=1.0).set_opacity(0.5)
        wheel_ring_inner = Circle(radius=R_WHEEL - 0.22, color=GOLD, stroke_width=0.7).set_opacity(0.35)

        # Tick marks at each sign boundary
        ticks = VGroup()
        for i in range(12):
            a = TAU * i / 12
            p_out = np.array([np.cos(a), np.sin(a), 0]) * (R_WHEEL + 0.22)
            p_in  = np.array([np.cos(a), np.sin(a), 0]) * (R_WHEEL - 0.22)
            ticks.add(Line(p_out, p_in, color=GOLD, stroke_width=1.0).set_opacity(0.6))

        # Zodiac symbol labels
        zod_labels = VGroup()
        for i, sym in enumerate(ZODIAC_SYMBOLS):
            a = TAU * i / 12 + TAU / 24      # centre of each sign slice
            pos = np.array([np.cos(a), np.sin(a), 0]) * R_WHEEL
            zod_labels.add(
                Text(sym, font_size=18, color=PALE_GOLD)
                .set_opacity(0.75)
                .move_to(pos)
            )

        zodiac_wheel = VGroup(wheel_ring_outer, wheel_ring_inner, ticks, zod_labels)

        # ════════════════════════════════════════════════════════════════════
        # LAYER 2 – MANDALA / FLOWER OF LIFE (mid-ring)
        # ════════════════════════════════════════════════════════════════════
        R_MAND = 1.55
        mandala_circles = VGroup()
        for i in range(6):
            a = TAU * i / 6
            cx, cy = R_MAND * np.cos(a), R_MAND * np.sin(a)
            mandala_circles.add(
                Circle(radius=R_MAND, color=LILAC, stroke_width=0.8)
                .set_opacity(0.18)
                .move_to([cx, cy, 0])
            )
        center_circle = Circle(radius=R_MAND, color=LILAC, stroke_width=0.8).set_opacity(0.18)
        mandala = VGroup(mandala_circles, center_circle)

        # Petal outlines (intersection arcs approximated by smaller circles)
        petal_ring = VGroup(*[
            Circle(radius=0.55, color=ROSE, stroke_width=0.7)
            .set_opacity(0.22)
            .move_to([0.78 * np.cos(TAU * i / 6), 0.78 * np.sin(TAU * i / 6), 0])
            for i in range(6)
        ])

        # ════════════════════════════════════════════════════════════════════
        # LAYER 3 – INNER DECORATIVE RING with gem dots
        # ════════════════════════════════════════════════════════════════════
        R_DECO = 2.1
        deco_ring = Circle(radius=R_DECO, color=GOLD, stroke_width=1.5).set_opacity(0.45)

        n_gems = 24
        gem_group = VGroup()
        for i in range(n_gems):
            a = TAU * i / n_gems
            pos = [R_DECO * np.cos(a), R_DECO * np.sin(a), 0]
            r   = 0.07 if i % 6 == 0 else 0.038
            c   = GOLD if i % 6 == 0 else PALE_GOLD
            op  = 0.95 if i % 6 == 0 else 0.55
            gem_group.add(Dot(point=pos, radius=r, color=c).set_opacity(op))

        # Diamond shapes at cardinal points
        def diamond(cx, cy, size=0.13, color=GOLD):
            pts = [[cx, cy+size,0],[cx+size,cy,0],[cx,cy-size,0],[cx-size,cy,0]]
            return Polygon(*pts, color=color, fill_opacity=0.9, stroke_width=0)

        cardinal_diamonds = VGroup(
            diamond( R_DECO, 0, color=GOLD),
            diamond(-R_DECO, 0, color=GOLD),
            diamond(0,  R_DECO, color=GOLD),
            diamond(0, -R_DECO, color=GOLD),
        )

        # ════════════════════════════════════════════════════════════════════
        # LAYER 4 – CENTRAL STARBURST
        # ════════════════════════════════════════════════════════════════════
        def starburst(n=16, r_out=0.62, r_in=0.26, color=GOLD, op=1.0):
            angles_o = np.linspace(PI/2, PI/2 + TAU, n, endpoint=False)
            angles_i = angles_o + TAU / (2 * n)
            verts = []
            for ao, ai in zip(angles_o, angles_i):
                verts.append([r_out*np.cos(ao), r_out*np.sin(ao), 0])
                verts.append([r_in *np.cos(ai), r_in *np.sin(ai), 0])
            return Polygon(*verts, color=color, fill_opacity=op, stroke_width=0)

        burst_glow1 = starburst(16, 0.80, 0.34, PALE_GOLD, 0.12)
        burst_glow2 = starburst(16, 0.70, 0.30, PALE_GOLD, 0.20)
        burst_main  = starburst(16, 0.60, 0.25, GOLD,      1.00)
        burst_inner = starburst(8,  0.30, 0.14, PALE_GOLD, 1.00)
        center_dot  = Dot(radius=0.07, color=WHITE).set_opacity(0.95)

        central_star = VGroup(burst_glow1, burst_glow2, burst_main, burst_inner, center_dot)

        # ════════════════════════════════════════════════════════════════════
        # LAYER 5 – CRESCENT MOON (top-right)
        # ════════════════════════════════════════════════════════════════════
        moon_o = Circle(radius=0.52, color=PALE_GOLD, fill_opacity=1.0, stroke_width=0)
        moon_i = Circle(radius=0.42, color=BG,        fill_opacity=1.0, stroke_width=0).shift(RIGHT*0.20)
        crescent = VGroup(moon_o, moon_i).move_to(UR * 2.9 + LEFT * 0.3 + DOWN * 0.1)

        # Small stars around moon
        moon_stars = VGroup(*[
            Dot(
                point=crescent.get_center() + [rng.uniform(-0.9,0.9), rng.uniform(-0.7,0.7), 0],
                radius=rng.uniform(0.025, 0.05),
                color=PALE_GOLD
            ).set_opacity(rng.uniform(0.4, 0.9))
            for _ in range(8)
        ])

        # ════════════════════════════════════════════════════════════════════
        # LAYER 6 – SHOOTING STAR paths (will animate)
        # ════════════════════════════════════════════════════════════════════
        def shooting_star(start, angle_deg, length=1.8):
            a = np.radians(angle_deg)
            end = start + length * np.array([np.cos(a), np.sin(a), 0])
            line = Line(start, end, color=WHITE, stroke_width=1.2).set_opacity(0.0)
            return line

        shoot1 = shooting_star(np.array([-6.5,  3.2, 0]), -25, 2.2)
        shoot2 = shooting_star(np.array([ 5.0,  3.8, 0]), -35, 1.8)
        shoot3 = shooting_star(np.array([-5.5, -2.8, 0]),  20, 2.0)

        # ════════════════════════════════════════════════════════════════════
        # LAYER 7 – CONSTELLATION LINES (corners)
        # ════════════════════════════════════════════════════════════════════
        def constellation(pts_local, origin, col=SILVER):
            pts = [np.array([x, y, 0]) + origin for x, y in pts_local]
            dots  = VGroup(*[Dot(p, radius=0.04, color=col).set_opacity(0.8) for p in pts])
            lines = VGroup(*[
                Line(pts[i], pts[i+1], color=col, stroke_width=0.9).set_opacity(0.30)
                for i in range(len(pts)-1)
            ])
            return VGroup(dots, lines)

        const_bl = constellation([(0,0),(0.5,0.6),(1.1,0.3),(1.6,0.9),(2.0,0.5)],
                                  np.array([-7.0, -3.8, 0]))
        const_tr = constellation([(0,0),(-0.4,0.5),(-1.0,0.2),(-1.4,0.7)],
                                  np.array([ 5.8,  2.8, 0]))
        const_tl = constellation([(0,0),(0.6,-0.4),(1.2,0.1),(0.9,-0.9)],
                                  np.array([-7.0,  2.5, 0]))

        # ════════════════════════════════════════════════════════════════════
        # LAYER 8 – MAIN TITLE TEXT
        # ════════════════════════════════════════════════════════════════════
        # Gradient-like effect: two overlapping texts slightly offset
        title_shadow = Text("AntoTarot", font="Georgia", weight=BOLD,
                            color=DEEP_ROSE).scale(1.55).set_opacity(0.35)
        title_main   = Text("AntoTarot", font="Georgia", weight=BOLD,
                            color=PALE_GOLD).scale(1.55)

        title_group = VGroup(title_shadow, title_main)
        title_shadow.move_to(UP * 0.62 + RIGHT * 0.03 + DOWN * 0.03)
        title_main.move_to(UP * 0.62)

        # Ornamental divider
        div_line  = Line(LEFT*2.4, RIGHT*2.4, color=GOLD, stroke_width=1.0).set_opacity(0.55)
        div_dot_l = Dot(point=div_line.get_left(),  radius=0.05, color=GOLD)
        div_dot_r = Dot(point=div_line.get_right(), radius=0.05, color=GOLD)
        divider = VGroup(div_line, div_dot_l, div_dot_r).move_to(ORIGIN + DOWN*0.12)

        # ════════════════════════════════════════════════════════════════════
        # LAYER 9 – SUBTITLE  "Iubire și Adevăr"
        # ════════════════════════════════════════════════════════════════════
        subtitle = Text("Iubire \u0219i Adev\u0103r",
                        font="Georgia", slant=ITALIC,
                        color=ROSE).scale(0.62).move_to(DOWN * 0.88)

        # Flanking small diamond accents
        sub_dia_l = diamond(-2.55, -0.88, size=0.09, color=ROSE)
        sub_dia_r = diamond( 2.55, -0.88, size=0.09, color=ROSE)
        sub_accents = VGroup(sub_dia_l, sub_dia_r)

        # ════════════════════════════════════════════════════════════════════
        # LAYER 10 – BOTTOM TAGLINE
        # ════════════════════════════════════════════════════════════════════
        tagline = Text("✦   Citește stelele, descoperă-ți destinul   ✦",
                       font="Georgia", slant=ITALIC,
                       color=TEAL).scale(0.27).move_to(DOWN * 1.62)

        # ════════════════════════════════════════════════════════════════════
        # ▸▸  ANIMATION SEQUENCE  ◂◂
        # ════════════════════════════════════════════════════════════════════

        # — 0. Instant background stars
        self.add(stars_bg)

        # — 1. Foreground stars sparkle in + constellations
        self.play(
            FadeIn(stars_fg, run_time=1.5),
            FadeIn(const_bl, run_time=1.8),
            FadeIn(const_tr, run_time=1.8),
            FadeIn(const_tl, run_time=1.8),
            FadeIn(crescent, run_time=1.2),
            FadeIn(moon_stars, run_time=1.4),
        )

        # — 2. Zodiac wheel draws in (create arc by arc feel via Create)
        self.play(
            Create(wheel_ring_outer, run_time=1.8),
            Create(wheel_ring_inner, run_time=1.8),
            lag_ratio=0.1
        )
        self.play(
            Create(ticks, run_time=0.8),
            FadeIn(zod_labels, run_time=1.0),
        )

        # — 3. Shooting stars streak across
        self.play(
            shoot1.animate.set_opacity(0.8),
            run_time=0.18
        )
        self.play(shoot1.animate.set_opacity(0), run_time=0.35)
        self.play(
            shoot2.animate.set_opacity(0.75),
            run_time=0.18
        )
        self.play(shoot2.animate.set_opacity(0), run_time=0.30)

        # — 4. Mandala blooms
        self.play(
            LaggedStart(
                *[GrowFromCenter(c) for c in mandala_circles],
                lag_ratio=0.12,
                run_time=1.2
            ),
            GrowFromCenter(center_circle, run_time=0.8),
        )
        self.play(FadeIn(petal_ring, run_time=0.6))

        # — 5. Inner deco ring + gems appear
        self.play(
            Create(deco_ring, run_time=1.0),
            LaggedStart(
                *[GrowFromCenter(g) for g in gem_group],
                lag_ratio=0.04,
                run_time=1.2
            ),
        )
        self.play(
            LaggedStart(
                *[GrowFromCenter(d) for d in cardinal_diamonds],
                lag_ratio=0.15,
                run_time=0.6
            )
        )

        # — 6. Central starburst explodes in
        self.play(GrowFromCenter(central_star, run_time=0.65))
        self.play(
            Flash(central_star, color=GOLD, flash_radius=0.95,
                  line_length=0.38, num_lines=16, run_time=0.7),
        )

        # — 7. Title shadow drifts in from below, then main title writes
        self.play(FadeIn(title_shadow, shift=UP*0.2, run_time=0.6))
        self.play(AddTextLetterByLetter(title_main, run_time=1.1))

        # — 8. Divider line sweeps in
        self.play(Create(divider, run_time=0.55))

        # — 9. Third shooting star while subtitle fades
        self.play(
            shoot3.animate.set_opacity(0.7),
            FadeIn(subtitle, shift=UP*0.12, run_time=0.7),
            run_time=0.4
        )
        self.play(
            shoot3.animate.set_opacity(0),
            GrowFromCenter(sub_accents, run_time=0.4),
        )

        # — 10. Tagline floats up
        self.play(FadeIn(tagline, shift=UP*0.1, run_time=0.7))

        # — 11. Everything gently breathes / rotates for a few seconds
        all_rings = VGroup(zodiac_wheel, deco_ring, gem_group, cardinal_diamonds)
        self.play(
            Rotate(all_rings, angle=TAU / 12, about_point=ORIGIN,
                   run_time=4.5, rate_func=linear),
            ScaleInPlace(central_star, 1.14,
                         run_time=1.2, rate_func=there_and_back),
        )

        # — 12. Starburst final pulse + brief hold
        self.play(
            Flash(central_star, color=PALE_GOLD, flash_radius=0.75,
                  line_length=0.25, num_lines=12, run_time=0.5),
        )
        self.wait(0.8)

        # — 13. Fade everything to black
        everything = VGroup(
            stars_bg, stars_fg,
            const_bl, const_tr, const_tl,
            crescent, moon_stars,
            zodiac_wheel,
            mandala, petal_ring,
            deco_ring, gem_group, cardinal_diamonds,
            central_star,
            title_group, divider,
            subtitle, sub_accents,
            tagline,
            shoot1, shoot2, shoot3,
        )
        self.play(FadeOut(everything, run_time=1.4))
        self.wait(0.2)
