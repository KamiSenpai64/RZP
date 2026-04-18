from manim import *
import numpy as np

class AstroTarotIntro(Scene):
    def construct(self):
        # ── Colour palette ──────────────────────────────────────────────
        DEEP_PURPLE  = "#1A0533"
        GOLD         = "#FFD700"
        SOFT_GOLD    = "#FFF0A0"
        STAR_WHITE   = "#EEE8FF"
        ACCENT_TEAL  = "#7FFFD4"

        # ── Background ──────────────────────────────────────────────────
        self.camera.background_color = DEEP_PURPLE

        # ── Stars (static scattered dots) ───────────────────────────────
        rng = np.random.default_rng(42)
        stars = VGroup(*[
            Dot(
                point=[rng.uniform(-7, 7), rng.uniform(-4, 4), 0],
                radius=rng.uniform(0.015, 0.05),
                color=STAR_WHITE,
            ).set_opacity(rng.uniform(0.3, 0.9))
            for _ in range(120)
        ])

        # ── Orbiting ring ───────────────────────────────────────────────
        orbit_ring = Circle(radius=1.9, color=GOLD, stroke_width=1.2)
        orbit_ring.set_opacity(0.35)

        # Small gems on the ring (used later for rotation effect)
        gem_angles = np.linspace(0, TAU, 12, endpoint=False)
        gems = VGroup(*[
            Dot(
                point=[1.9 * np.cos(a), 1.9 * np.sin(a), 0],
                radius=0.045,
                color=GOLD,
            ).set_opacity(0.7)
            for a in gem_angles
        ])

        # ── Moon crescent (top-left accent) ─────────────────────────────
        moon_outer = Circle(radius=0.55, color=SOFT_GOLD, fill_opacity=1)
        moon_inner = Circle(radius=0.44, color=DEEP_PURPLE, fill_opacity=1).shift(RIGHT * 0.18)
        crescent = VGroup(moon_outer, moon_inner).shift(UL * 2.6)

        # ── Central star / asterisk ──────────────────────────────────────
        def make_star_burst(n_points=8, r_outer=0.55, r_inner=0.22, color=GOLD):
            angles_outer = np.linspace(PI / 2, PI / 2 + TAU, n_points, endpoint=False)
            angles_inner = angles_outer + TAU / (2 * n_points)
            verts = []
            for ao, ai in zip(angles_outer, angles_inner):
                verts.append([r_outer * np.cos(ao), r_outer * np.sin(ao), 0])
                verts.append([r_inner * np.cos(ai), r_inner * np.sin(ai), 0])
            return Polygon(*verts, color=color, fill_opacity=1, stroke_width=0)

        star_burst = make_star_burst(color=GOLD)
        star_glow  = make_star_burst(r_outer=0.65, r_inner=0.28, color=SOFT_GOLD).set_opacity(0.25)
        central_star = VGroup(star_glow, star_burst)

        # ── Main text ────────────────────────────────────────────────────
        astro_text = Text(
            "ASTRO",
            font="Georgia",
            weight=BOLD,
            color=SOFT_GOLD,
        ).scale(1.45)

        tarot_text = Text(
            "TAROT",
            font="Georgia",
            weight=BOLD,
            color=GOLD,
        ).scale(1.45)

        # Stack vertically, tightly
        astro_text.move_to(UP * 0.52)
        tarot_text.move_to(DOWN * 0.52)
        title_group = VGroup(astro_text, tarot_text)

        # Thin divider line between words
        divider = Line(LEFT * 1.8, RIGHT * 1.8, color=GOLD, stroke_width=1.2).set_opacity(0.6)

        # ── Tagline ───────────────────────────────────────────────────────
        tagline = Text(
            "✦  read the stars, reveal your path  ✦",
            font="Georgia",
            color=ACCENT_TEAL,
            slant=ITALIC,
        ).scale(0.32).next_to(tarot_text, DOWN * 2.2)

        # ── Corner constellation dots ─────────────────────────────────────
        def corner_constellation(shift_vec):
            pts = [(0,0), (0.35, 0.55), (0.7, 0.3), (1.0, 0.8)]
            dots = VGroup(*[Dot(point=[x, y, 0], radius=0.04, color=STAR_WHITE).set_opacity(0.7)
                            for x, y in pts])
            lines = VGroup(*[
                Line(dots[i].get_center(), dots[i+1].get_center(),
                     color=STAR_WHITE, stroke_width=0.8).set_opacity(0.35)
                for i in range(len(pts)-1)
            ])
            return VGroup(dots, lines).shift(shift_vec)

        const_br = corner_constellation(DR * 2.5 + LEFT * 0.5)
        const_ul = corner_constellation(UL * 2.8 + RIGHT * 0.9).flip(UP)

        # ════════════════════════════════════════════════════════════════
        # ANIMATION SEQUENCE
        # ════════════════════════════════════════════════════════════════

        # 1) Fade in background elements
        self.play(
            FadeIn(stars, run_time=1.2),
            FadeIn(crescent, run_time=1.2),
            FadeIn(const_br, run_time=1.2),
            FadeIn(const_ul, run_time=1.2),
        )

        # 2) Draw orbiting ring
        self.play(
            Create(orbit_ring, run_time=1.4),
            FadeIn(gems, run_time=1.4),
        )

        # 3) Burst in central star
        central_star.scale(0)
        self.play(
            central_star.animate.scale(1 / 0.001 * 0.001 + 1),  # reset
        )
        central_star.scale(0)
        self.play(
            ScaleInPlace(central_star, 1, rate_func=rush_from),
            run_time=0.01
        )
        # Simple grow + flash
        self.play(
            GrowFromCenter(central_star, run_time=0.7),
        )
        self.play(
            Flash(central_star, color=GOLD, flash_radius=0.8,
                  line_length=0.3, num_lines=12, run_time=0.6),
        )

        # 4) Reveal "ASTRO" — write from left
        self.play(
            AddTextLetterByLetter(astro_text, run_time=0.9),
        )

        # 5) Draw divider, then reveal "TAROT"
        self.play(Create(divider, run_time=0.4))
        self.play(
            AddTextLetterByLetter(tarot_text, run_time=0.9),
        )

        # 6) Fade in tagline
        self.play(FadeIn(tagline, shift=UP * 0.15, run_time=0.8))

        # 7) Slow spin of ring + gems together (held pose)
        ring_gems = VGroup(orbit_ring, gems)
        self.play(
            Rotate(ring_gems, angle=TAU, about_point=ORIGIN, run_time=6, rate_func=linear),
            title_group.animate(run_time=0.5).set_opacity(1),  # subtle hold
            run_time=3,
        )

        # 8) Gentle pulse on star
        self.play(
            ScaleInPlace(central_star, 1.18, run_time=0.45, rate_func=there_and_back),
        )

        # 9) Hold for a moment, then fade everything out
        self.wait(0.6)
        self.play(
            FadeOut(VGroup(
                stars, crescent, orbit_ring, gems,
                const_br, const_ul, central_star,
                title_group, divider, tagline
            ), run_time=1.2)
        )
        self.wait(0.3)


# ── Entry point ──────────────────────────────────────────────────────────────
# Render with:
#   manim -pqh astro_tarot_intro.py AstroTarotIntro
#
# Quality flags:
#   -ql  → 480p (fast preview)
#   -qm  → 720p
#   -qh  → 1080p
#   -qk  → 4K
