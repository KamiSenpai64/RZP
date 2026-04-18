from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
#  AntoTarot  –  Dark Moonlit Mystical
#  Render:  manim -pqh anto_tarot_intro.py AntoTarotIntro
# ─────────────────────────────────────────────────────────────────────────────

class AntoTarotIntro(Scene):
    def construct(self):
        # ── Palette  (cold, moonlit, no gold/sun) ────────────────────────
        BG          = "#03060F"
        MOONWHITE   = "#E8F0FF"
        SILVER      = "#B8C8F0"
        ICE         = "#D0EAFF"
        MIST        = "#6080B0"
        DEEP_BLUE   = "#0A1535"
        PALE_VIOLET = "#C8B8FF"
        DARK_TEAL   = "#0D3040"
        TEAL_GLOW   = "#40C8C0"

        self.camera.background_color = BG
        rng = np.random.default_rng(13)

        # ── Mist veils ───────────────────────────────────────────────────
        mist1 = Ellipse(width=10, height=3.5, color=DEEP_BLUE,
                        fill_opacity=0.55, stroke_width=0).move_to(DOWN * 0.3)
        mist2 = Ellipse(width=7,  height=2.2, color=DARK_TEAL,
                        fill_opacity=0.30, stroke_width=0).move_to(UP * 0.4)

        # ── Star field ───────────────────────────────────────────────────
        def make_stars(n, r_lo, r_hi, op_lo, op_hi, col=MOONWHITE):
            return VGroup(*[
                Dot(
                    point=[rng.uniform(-7.5, 7.5), rng.uniform(-4.3, 4.3), 0],
                    radius=rng.uniform(r_lo, r_hi),
                    color=col,
                ).set_opacity(rng.uniform(op_lo, op_hi))
                for _ in range(n)
            ])

        stars_dim    = make_stars(180, 0.010, 0.028, 0.10, 0.40, SILVER)
        stars_mid    = make_stars(50,  0.030, 0.055, 0.40, 0.80, ICE)
        stars_bright = make_stars(12,  0.055, 0.085, 0.70, 1.00, MOONWHITE)

        # ── Moon phase row ───────────────────────────────────────────────
        def crescent(phase=0.0, r=0.28, pos=ORIGIN):
            outer = Circle(radius=r, color=MOONWHITE, fill_opacity=1, stroke_width=0)
            if phase >= 0.99:
                return outer.move_to(pos)
            offset = r * (1 - 2 * phase) * 1.1
            inner  = Circle(radius=r * 0.92, color=BG, fill_opacity=1, stroke_width=0)
            inner.shift(RIGHT * offset)
            return VGroup(outer, inner).move_to(pos)

        moon_phases = VGroup(
            crescent(0.08, 0.22, UP*3.4 + LEFT*3.2),
            crescent(0.28, 0.26, UP*3.4 + LEFT*1.6),
            crescent(1.00, 0.32, UP*3.4),
            crescent(0.72, 0.26, UP*3.4 + RIGHT*1.6).flip(RIGHT),
            crescent(0.92, 0.22, UP*3.4 + RIGHT*3.2).flip(RIGHT),
        )
        phase_line = Line(UP*3.4 + LEFT*4.0, UP*3.4 + RIGHT*4.0,
                          color=SILVER, stroke_width=0.5).set_opacity(0.25)

        # ── Tarot card frame ─────────────────────────────────────────────
        FRAME_W, FRAME_H = 5.8, 7.4
        frame_rect  = Rectangle(width=FRAME_W, height=FRAME_H,
                                 color=SILVER, stroke_width=1.2).set_opacity(0.40)
        frame_inner = Rectangle(width=FRAME_W-0.36, height=FRAME_H-0.36,
                                 color=SILVER, stroke_width=0.5).set_opacity(0.20)

        def corner_cross(cx, cy, size=0.22):
            h  = Line([cx-size,cy,0],[cx+size,cy,0], color=SILVER, stroke_width=1.0).set_opacity(0.7)
            v  = Line([cx,cy-size,0],[cx,cy+size,0], color=SILVER, stroke_width=1.0).set_opacity(0.7)
            d1 = Line([cx-size*.6,cy-size*.6,0],[cx+size*.6,cy+size*.6,0],
                      color=SILVER, stroke_width=0.6).set_opacity(0.45)
            d2 = Line([cx+size*.6,cy-size*.6,0],[cx-size*.6,cy+size*.6,0],
                      color=SILVER, stroke_width=0.6).set_opacity(0.45)
            return VGroup(h, v, d1, d2)

        hw, hh = FRAME_W/2, FRAME_H/2
        corners = VGroup(
            corner_cross(-hw,  hh), corner_cross( hw,  hh),
            corner_cross(-hw, -hh), corner_cross( hw, -hh),
        )
        card_frame = VGroup(frame_rect, frame_inner, corners)

        # ── Hexagram / sacred geometry ───────────────────────────────────
        R_TRI = 1.10

        def triangle_pts(r, rotation=0):
            return [[r*np.cos(PI/2+rotation+TAU*i/3),
                     r*np.sin(PI/2+rotation+TAU*i/3), 0] for i in range(3)]

        tri_up   = Polygon(*triangle_pts(R_TRI, 0),
                           color=PALE_VIOLET, stroke_width=0.9, fill_opacity=0).set_opacity(0.50)
        tri_down = Polygon(*triangle_pts(R_TRI, PI),
                           color=TEAL_GLOW, stroke_width=0.9, fill_opacity=0).set_opacity(0.50)
        hex_circle = Circle(radius=R_TRI, color=SILVER, stroke_width=0.5).set_opacity(0.20)
        inner_hex  = Circle(radius=0.55,  color=SILVER, stroke_width=0.5).set_opacity(0.18)
        geometry   = VGroup(hex_circle, inner_hex, tri_up, tri_down)

        # ── Floating particles ───────────────────────────────────────────
        particles = VGroup(*[
            Dot(point=[rng.uniform(-2.5,2.5), rng.uniform(-3.0,3.0), 0],
                radius=rng.uniform(0.012,0.030), color=ICE)
            .set_opacity(rng.uniform(0.05, 0.28))
            for _ in range(55)
        ])

        # ── Eye of Providence ────────────────────────────────────────────
        eye_outer = Ellipse(width=1.10, height=0.52, color=SILVER,
                            stroke_width=0.9, fill_opacity=0).set_opacity(0.55)
        pupil  = Circle(radius=0.16, color=PALE_VIOLET, fill_opacity=0.6,
                        stroke_width=0.7).set_opacity(0.80)
        iris   = Circle(radius=0.24, color=SILVER, stroke_width=0.5,
                        fill_opacity=0).set_opacity(0.35)
        lash_lines = VGroup(*[
            Line([0.55*np.cos(PI-PI*i/8), 0.28*np.sin(PI-PI*i/8),0],
                 [0.73*np.cos(PI-PI*i/8), 0.40*np.sin(PI-PI*i/8),0],
                 color=SILVER, stroke_width=0.6).set_opacity(0.30)
            for i in range(9)
        ])
        eye_group = VGroup(eye_outer, iris, pupil, lash_lines)

        # ── Title ────────────────────────────────────────────────────────
        title = Text("AntoTarot", font="Georgia", weight=BOLD,
                     color=MOONWHITE).scale(1.50).move_to(UP * 0.55)
        title_underline = Line(
            title.get_left()  + DOWN*0.12,
            title.get_right() + DOWN*0.12,
            color=PALE_VIOLET, stroke_width=1.0
        ).set_opacity(0.50)

        # ── Divider ──────────────────────────────────────────────────────
        dash_l  = Line(LEFT*2.2,  LEFT*0.35,  color=SILVER, stroke_width=0.8).set_opacity(0.45)
        dash_r  = Line(RIGHT*0.35, RIGHT*2.2, color=SILVER, stroke_width=0.8).set_opacity(0.45)
        mid_dot = Dot(ORIGIN, radius=0.045, color=PALE_VIOLET).set_opacity(0.9)
        divider = VGroup(dash_l, mid_dot, dash_r).move_to(DOWN * 0.05)

        # ── Subtitle ─────────────────────────────────────────────────────
        subtitle = Text("Iubire \u0219i Adev\u0103r",
                        font="Georgia", slant=ITALIC,
                        color=PALE_VIOLET).scale(0.62).move_to(DOWN * 0.78)

        # ── Rune row ─────────────────────────────────────────────────────
        rune_row = Text("\u169b  \u1681  \u1682  \u1683  \u1684  \u1685  \u1686  \u1687  \u1688  \u1689  \u169b",
                        font_size=14, color=MIST).set_opacity(0.45).move_to(DOWN * 1.55)

        # ════════════════════════════════════════════════════════════════
        # ANIMATION
        # ════════════════════════════════════════════════════════════════

        self.play(
            FadeIn(mist1, run_time=2.0),
            FadeIn(mist2, run_time=2.0),
            FadeIn(stars_dim, run_time=2.0),
        )
        self.play(
            FadeIn(stars_mid,    run_time=1.2),
            FadeIn(stars_bright, run_time=1.0),
        )
        self.play(
            FadeIn(phase_line, run_time=0.6),
            LaggedStart(*[FadeIn(m, shift=DOWN*0.25) for m in moon_phases],
                        lag_ratio=0.18, run_time=1.4),
        )
        self.play(Create(frame_rect, run_time=1.6))
        self.play(
            Create(frame_inner, run_time=0.8),
            LaggedStart(*[FadeIn(c) for c in corners],
                        lag_ratio=0.2, run_time=0.8),
        )
        self.play(FadeIn(particles, run_time=1.5))
        self.play(Create(hex_circle, run_time=0.8))
        self.play(
            Create(tri_up,   run_time=0.9),
            Create(tri_down, run_time=0.9),
        )
        self.play(Create(inner_hex, run_time=0.5))
        self.play(GrowFromCenter(eye_group, run_time=0.9))
        self.play(
            Flash(pupil, color=TEAL_GLOW, flash_radius=0.45,
                  line_length=0.18, num_lines=10, run_time=0.55),
        )
        self.play(AddTextLetterByLetter(title, run_time=1.2))
        self.play(Create(title_underline, run_time=0.5))
        self.play(
            Create(dash_l,  run_time=0.5),
            Create(dash_r,  run_time=0.5),
            GrowFromCenter(mid_dot, run_time=0.3),
        )
        self.play(FadeIn(subtitle, shift=UP*0.12, run_time=0.9))
        self.play(FadeIn(rune_row, run_time=0.8))
        self.play(
            Rotate(tri_up,   angle= TAU/12, about_point=ORIGIN,
                   run_time=3.5, rate_func=linear),
            Rotate(tri_down, angle=-TAU/12, about_point=ORIGIN,
                   run_time=3.5, rate_func=linear),
            ScaleInPlace(pupil, 1.25, run_time=1.0, rate_func=there_and_back),
        )
        self.wait(0.7)
        self.play(
            FadeOut(VGroup(
                mist1, mist2,
                stars_dim, stars_mid, stars_bright,
                moon_phases, phase_line,
                card_frame, particles,
                geometry, eye_group,
                title, title_underline,
                divider, subtitle, rune_row,
            ), run_time=1.5)
        )
        self.wait(0.2)
