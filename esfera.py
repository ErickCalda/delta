from manim import *
import numpy as np

class DiferencialEsfera(Scene):
    def construct(self):

        # =========================================
        # 1. LEYENDA EXPLICATIVA (Esquina Superior Izquierda)
        # =========================================
        leyenda = VGroup(
            Tex(r"Curva Azul: Volumen real del tanque ($V$)").set_color(BLUE),
            Tex(r"Recta Amarilla: Aproximación por diferencial").set_color(YELLOW),
            Tex(r"Línea Verde ($dr$): Error de medición en el radio").set_color(GREEN),
            Tex(r"Línea Naranja ($dV$): Error propagado estimado").set_color(ORANGE),
            Tex(r"Línea Roja: Margen de error de la aproximación ($\Delta V - dV$)").set_color(RED)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.50).to_corner(UL)

        # =========================================
        # 2. EJES Y ESCALA INDUSTRIAL
        # =========================================
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 1200, 200],
            x_length=7,   
            y_length=4.5, 
            axis_config={"color": WHITE}
        ).to_edge(DOWN).shift(RIGHT * 0.5) 

        labels = axes.get_axis_labels(
            x_label="r\\text{ (m)}",
            y_label="V\\text{ (m}^3\text{)}"
        )

        # =========================================
        # 3. FUNCIÓN DEL VOLUMEN
        # =========================================
        graph = axes.plot(lambda r: (4/3) * np.pi * r**3, x_range=[0, 6.5], color=BLUE)
        formula = MathTex(r"V(r)=\frac{4}{3}\pi r^3").to_corner(UR)

        # =========================================
        # 4. VALORES DEL TANQUE REAL
        # =========================================
        r0 = 4.0 
        v0 = (4/3) * np.pi * r0**3
        punto = Dot(axes.coords_to_point(r0, v0), color=WHITE)

        # =========================================
        # 5. RECTA TANGENTE (Diferencial)
        # =========================================
        pendiente = 4 * np.pi * r0**2 
        line_func = lambda r: pendiente * (r - r0) + v0
        tangent = axes.plot(line_func, x_range=[r0 - 1.5, r0 + 2.5], color=YELLOW)

        # =========================================
        # 6. REPRESENTACIÓN DE ERRORES
        # =========================================
        dr = 1.0 
        r_error = r0 + dr
        v_aproximado = line_func(r_error) 
        v_real = (4/3) * np.pi * r_error**3 

        p_base = axes.coords_to_point(r0, v0)
        p_esquina = axes.coords_to_point(r_error, v0)
        p_alto = axes.coords_to_point(r_error, v_aproximado)
        p_real = axes.coords_to_point(r_error, v_real) 

        linea_dr = DashedLine(p_base, p_esquina, color=GREEN)
        linea_dv = DashedLine(p_esquina, p_alto, color=ORANGE)
        linea_error_aprox = Line(p_alto, p_real, color=RED, stroke_width=5)

        label_dr = MathTex("dr = 1m").next_to(linea_dr, DOWN, buff=0.1).scale(0.6).set_color(GREEN)
        label_dv = MathTex("dV").next_to(linea_dv, RIGHT, buff=0.1).scale(0.7).set_color(ORANGE)
        label_error = MathTex(r"\text{Falla}").next_to(linea_error_aprox, LEFT, buff=0.1).scale(0.5).set_color(RED)

# =========================================
        # 7. FORMULAS ORGANIZADAS (SUBIDAS PARA QUE NO CHOQUEN)
        # =========================================
        formula_dif = MathTex(r"dV = 4\pi r^2 dr").set_color(ORANGE).scale(0.7)
        formula_falla = MathTex(r"\text{Falla} = \Delta V - dV").set_color(RED).scale(0.7)
        
        # Agrupamos las fórmulas y las posicionamos en la esquina inferior derecha
        # .shift(UP * 1.5) es lo que hará que "suban" y se alejen del eje X y del texto "r (m)"
        grupo_formulas = VGroup(formula_dif, formula_falla).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR).shift(UP * 1.5)
        # =========================================
        # 8. ANIMACIONES PULIDAS
        # =========================================
        self.play(Write(leyenda), run_time=2) 
        self.play(Create(axes), Write(labels), run_time=1.5)
        self.play(Create(graph), Write(formula), run_time=1.5)
        self.play(FadeIn(punto), run_time=1)
        self.play(Create(tangent), run_time=1.5)

        self.play(Create(linea_dr), Write(label_dr), run_time=1)
        self.play(Create(linea_dv), Write(label_dv), run_time=1)
        
        # Animamos el grupo de fórmulas ordenado y limpio
        self.play(Write(grupo_formulas), run_time=1.5)
        
        # Animamos el fallo final
        self.play(Create(linea_error_aprox), Write(label_error), run_time=1)

        self.wait(4)