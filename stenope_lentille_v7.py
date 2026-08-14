from manim import *
import numpy as np

# ============================================================
# STÉNOPÉ -> LENTILLE
# Version 7 : propagation rectiligne, écran diffusant explicite,
#             sténopé plus petit, reconstruction de la fleur.
#
# Rendu rapide :
#   manim -pql stenope_lentille_v7.py StenopeVersLentilleV7
#
# Rendu HD :
#   manim -pqh stenope_lentille_v7.py StenopeVersLentilleV7
# ============================================================


class StenopeVersLentilleV7(Scene):

    def make_eye(self, center, scale=1.0):
        c = np.array(center, dtype=float)
        white = Ellipse(width=1.15*scale, height=0.58*scale, stroke_width=2.2)
        iris = Circle(radius=0.16*scale, stroke_width=2.0)
        pupil = Circle(radius=0.115*scale, fill_opacity=1, stroke_width=0)
        eye = VGroup(white, iris, pupil)
        eye.move_to(c)
        return eye

    def divergent_bundle_to_pupil(self, source, eye, n=7,
                                    opacity=0.68, width=1.35,
                                    show_cone=True):
        """
        PINCEAU entrant dans l'œil.

        Le point source émet dans toutes les directions. L'œil ne reçoit
        que le sous-ensemble des rayons interceptés par la pupille :
        on le représente par un faisceau divergent nettement visible,
        limité par les bords de la pupille.

        Les rayons restent rectilignes jusqu'à l'œil.
        """
        source = np.array(source, dtype=float)
        pupil = eye[2]
        c = pupil.get_center()
        r = pupil.width / 2

        upper = c + np.array([0.0, 0.92*r, 0.0])
        lower = c + np.array([0.0, -0.92*r, 0.0])

        bundle = VGroup()

        # Une légère nappe rend le pinceau immédiatement perceptible.
        if show_cone:
            cone = Polygon(
                source, upper, lower,
                stroke_width=0,
                fill_opacity=0.055
            )
            bundle.add(cone)

        # Plusieurs rayons distincts entrent en différents points
        # de l'ouverture pupillaire.
        for dy in np.linspace(-0.92*r, 0.92*r, n):
            target = c + np.array([0.0, dy, 0.0])
            ray = Line(source, target, stroke_width=width)
            ray.set_opacity(opacity)
            bundle.add(ray)

        return bundle

    def make_flower(self, center, scale=1.0):
        c = np.array(center, dtype=float)
        petals = VGroup()
        r = 0.22 * scale
        for ang in np.linspace(0, TAU, 7, endpoint=False):
            p = Circle(radius=r, stroke_width=1.8)
            p.move_to(c + np.array([0.28*np.cos(ang), 0.28*np.sin(ang), 0])*scale)
            petals.add(p)

        heart = Circle(radius=0.12*scale, fill_opacity=0.10, stroke_width=1.6)
        heart.move_to(c)
        stem = Line(c + DOWN*0.35*scale, c + DOWN*1.1*scale, stroke_width=2)
        leaf1 = ArcBetweenPoints(
            c + DOWN*0.62*scale,
            c + np.array([-0.40, -0.72, 0])*scale,
            angle=0.9,
            stroke_width=1.5
        )
        leaf2 = ArcBetweenPoints(
            c + DOWN*0.80*scale,
            c + np.array([0.36, -0.92, 0])*scale,
            angle=-0.9,
            stroke_width=1.5
        )
        return VGroup(petals, heart, stem, leaf1, leaf2)

    def make_aperture(self, x, half_gap, height=5.0, width=0.22):
        upper_h = height/2 - half_gap
        lower_h = height/2 - half_gap

        upper = Rectangle(width=width, height=upper_h,
                          fill_opacity=0.25, stroke_width=1.5)
        lower = Rectangle(width=width, height=lower_h,
                          fill_opacity=0.25, stroke_width=1.5)

        upper.move_to([x, half_gap + upper_h/2, 0])
        lower.move_to([x, -half_gap - lower_h/2, 0])
        return VGroup(upper, lower)

    def make_screen(self, x, height=4.5):
        veil = Rectangle(width=0.18, height=height,
                         fill_opacity=0.08, stroke_opacity=0)
        veil.move_to([x, 0, 0])
        line = Line([x, -height/2, 0], [x, height/2, 0], stroke_width=4)
        return VGroup(veil, line)

    def make_lens(self, x, height=3.9):
        top = np.array([x, height/2, 0])
        bot = np.array([x, -height/2, 0])
        left = ArcBetweenPoints(top, bot, angle=0.28)
        right = ArcBetweenPoints(bot, top, angle=0.28)
        lens = VGroup(left, right)
        lens.set_stroke(width=3)
        return lens

    def make_screen_inset(self, center):
        box = RoundedRectangle(width=2.05, height=2.15,
                               corner_radius=0.08,
                               stroke_width=1.5,
                               fill_opacity=0.03)
        box.move_to(center)
        label = Text("vue de face de l'écran", font_size=18)
        label.next_to(box, UP, buff=0.08)
        return VGroup(box, label)

    def screen_flower_from_object(self, object_flower, center,
                                  scale_factor=0.505):
        """
        Copie EXACTE de l'objet-fleur pour la vue de face de l'écran.

        On ne redessine pas une autre fleur : on copie l'objet lui-même,
        on le réduit, on le renverse de 180° puis on le place sur l'écran.
        Les pétales restent donc non remplis, le cœur garde son remplissage,
        et tous les traits sont identiques à ceux de l'objet.
        """
        f = object_flower.copy()
        f.scale(scale_factor)
        f.rotate(PI, about_point=f.get_center())
        f.move_to(np.array(center, dtype=float))
        return f

    def attenuate_preserving_style(self, mob, opacity):
        """
        Diminue la visibilité sans transformer les contours vides
        en surfaces remplies.

        set_opacity() sur un Circle de Manim modifie aussi son fill_opacity ;
        c'est précisément ce qui remplissait les pétales dans la version
        précédente. Ici on atténue séparément contour et remplissage.
        """
        for sm in mob.family_members_with_points():
            # Conserver la structure plein/vide d'origine.
            original_fill = sm.get_fill_opacity()
            sm.set_stroke(opacity=opacity)
            if original_fill > 0:
                sm.set_fill(opacity=original_fill * opacity)
            else:
                sm.set_fill(opacity=0)
        return mob

    def make_blurred_flower(self, object_flower, center, scale_factor,
                            blur_radius, opacity=0.13):
        """
        Figure de sténopé : superposition de copies EXACTES de l'objet,
        légèrement translatées. Chaque copie conserve les mêmes contours
        et les mêmes zones pleines/vides que l'objet.
        """
        offsets = [
            (0, 0),
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (0.70, 0.70), (-0.70, 0.70),
            (0.70, -0.70), (-0.70, -0.70)
        ]

        copies = VGroup()
        for dx, dy in offsets:
            f = self.screen_flower_from_object(
                object_flower, center, scale_factor
            )
            f.shift(np.array([dx*blur_radius, dy*blur_radius, 0]))
            self.attenuate_preserving_style(f, opacity)
            copies.add(f)

        return copies

    def make_sharp_flower(self, object_flower, center, scale_factor):
        """
        Image stigmatique idéale : une unique copie exacte de l'objet,
        renversée et réduite. Aucun flou, aucune copie décalée.
        """
        return self.screen_flower_from_object(
            object_flower, center, scale_factor
        )

    def x_intersection_of_line(self, p1, p2, x):
        p1 = np.array(p1, dtype=float)
        p2 = np.array(p2, dtype=float)
        t = (x - p1[0]) / (p2[0] - p1[0])
        return p1 + t * (p2 - p1)

    def pinhole_bundle(self, obj_point, aperture_x, half_gap, screen_x,
                       n=7, opacity=0.34, width=1.35):
        ys = np.linspace(-half_gap, half_gap, n)
        rays = VGroup()
        hits = []
        for y in ys:
            hole_point = np.array([aperture_x, y, 0.0])
            hit = self.x_intersection_of_line(obj_point, hole_point, screen_x)
            hits.append(hit)
            before = Line(obj_point, hole_point, stroke_width=width)
            after = Line(hole_point, hit, stroke_width=width)
            before.set_opacity(opacity)
            after.set_opacity(opacity)
            rays.add(before, after)
        return rays, np.array(hits)

    def ideal_lens_bundle(self, obj_point, lens_x, image_point,
                          heights, opacity=0.42, width=1.45):
        rays = VGroup()
        for h in heights:
            on_lens = np.array([lens_x, h, 0.0])
            before = Line(obj_point, on_lens, stroke_width=width)
            after = Line(on_lens, image_point, stroke_width=width)
            before.set_opacity(opacity)
            after.set_opacity(opacity)
            rays.add(before, after)
        return rays

    def patch_from_hits(self, hits, x, min_h=0.06):
        ymin = float(hits[:, 1].min())
        ymax = float(hits[:, 1].max())
        h = max(ymax - ymin, min_h)
        rect = Rectangle(width=0.11, height=h,
                         fill_opacity=0.34, stroke_width=0)
        rect.move_to([x, (ymin+ymax)/2, 0])
        return rect

    def construct(self):
        x_obj = -5.25
        x_opt = -0.20
        x_screen_pinhole = 3.05

        focal = 1.95
        object_distance = x_opt - x_obj
        image_distance = focal * object_distance / (object_distance - focal)
        x_screen_lens = x_opt + image_distance
        gamma_lens = -image_distance / object_distance

        A = np.array([x_obj, 0.755, 0.0])
        B = np.array([x_obj, -0.80, 0.0])
        C = np.array([x_obj, 0.10, 0.0])

        eye_center = np.array([5.55, 1.75, 0.0])

        # 1. VOIR L'OBJET
        flower = self.make_flower([x_obj, 0.23, 0], scale=1.05)
        eye = self.make_eye(eye_center, scale=0.9)
        title = Text("Voir un objet : l'œil doit recevoir de la lumière",
                     font_size=30).to_edge(UP)

        self.play(FadeIn(title), FadeIn(flower), FadeIn(eye))
        self.wait(0.4)

        dots = VGroup(Dot(A, radius=0.055),
                      Dot(B, radius=0.055),
                      Dot(C, radius=0.050))
        labels = VGroup(Text("A", font_size=23).next_to(A, UL, buff=0.08),
                        Text("B", font_size=23).next_to(B, DL, buff=0.08))
        self.play(FadeIn(dots), FadeIn(labels))

        diffuse = VGroup()
        for P in [A, B]:
            for y_end in [-2.6, -1.4, 0.1, 1.2, 2.7]:
                end = np.array([1.6, y_end, 0.0])
                ray = Line(P, end, stroke_width=1.0)
                ray.set_opacity(0.18)
                diffuse.add(ray)
        self.play(Create(diffuse), run_time=1.2)

        pupil = eye[2].get_center()
        to_eye = VGroup(
            self.divergent_bundle_to_pupil(A, eye, n=5,
                                            opacity=0.72, width=1.45),
            self.divergent_bundle_to_pupil(B, eye, n=5,
                                            opacity=0.72, width=1.45),
            self.divergent_bundle_to_pupil(C, eye, n=4,
                                            opacity=0.52, width=1.25),
        )
        self.play(Create(to_eye), run_time=1.3)

        received = Text("L'œil reçoit de la lumière issue de l'objet",
                        font_size=23)
        received.next_to(eye, DOWN, buff=0.22).shift(LEFT*0.85)
        self.play(FadeIn(received))
        self.wait(0.8)

        # 2. STÉNOPÉ
        self.play(FadeOut(diffuse), FadeOut(to_eye), FadeOut(received),
                  Transform(title,
                            Text("Sténopé : une ouverture finie sélectionne des rayons",
                                 font_size=29).to_edge(UP)))

        # On démarre directement avec l'ancien deuxième diamètre.
        hole_half_1 = 0.13
        aperture = self.make_aperture(x_opt, hole_half_1)
        screen = self.make_screen(x_screen_pinhole)
        hole_label = Text("trou", font_size=22).next_to(aperture, UP, buff=0.10)
        screen_label = Text("écran diffusant", font_size=20)
        screen_label.next_to(screen, DOWN, buff=0.10)

        self.play(FadeIn(aperture), FadeIn(screen),
                  FadeIn(hole_label), FadeIn(screen_label))

        bundleA, hitsA = self.pinhole_bundle(A, x_opt, hole_half_1,
                                             x_screen_pinhole, n=7)
        bundleB, hitsB = self.pinhole_bundle(B, x_opt, hole_half_1,
                                             x_screen_pinhole, n=7)
        self.play(Create(bundleA), run_time=1.0)
        self.play(Create(bundleB), run_time=1.0)

        patchA = self.patch_from_hits(hitsA, x_screen_pinhole)
        patchB = self.patch_from_hits(hitsB, x_screen_pinhole)
        self.play(FadeIn(patchA), FadeIn(patchB))

        caption_patch = Text("Un point-objet donne une tache sur l'écran",
                             font_size=22).to_edge(DOWN)
        self.play(FadeIn(caption_patch))

        # Inset : vue de face de l'écran, où la fleur peut être réellement visible.
        inset_center = np.array([5.15, -1.45, 0])
        inset = self.make_screen_inset(inset_center)
        blur1 = self.make_blurred_flower(
            object_flower=flower,
            center=inset_center + DOWN*0.05,
            scale_factor=0.505,
            blur_radius=0.105,
            opacity=0.14
        )
        self.play(FadeIn(inset), FadeIn(blur1), run_time=1.0)
        self.wait(0.6)

        # Les rayons incidents s'arrêtent sur l'écran.
        # L'écran diffuse ensuite la lumière : ce sont de nouveaux trajets.
        scatter_label = Text("l'écran rediffuse vers l'œil", font_size=18)
        scatter_label.next_to(eye, DOWN, buff=0.16).shift(LEFT*0.60)
        scattered = VGroup(
            self.divergent_bundle_to_pupil(
                patchA.get_center(), eye, n=7,
                opacity=0.72, width=1.35
            ),
            self.divergent_bundle_to_pupil(
                patchB.get_center(), eye, n=7,
                opacity=0.72, width=1.35
            )
        )
        self.play(FadeIn(scatter_label), Create(scattered), run_time=0.9)
        self.wait(0.7)

        # On referme encore le trou.
        self.play(Transform(title,
                            Text("En refermant le trou, chaque tache se resserre",
                                 font_size=29).to_edge(UP)))

        hole_half_2 = 0.055
        aperture_small = self.make_aperture(x_opt, hole_half_2)
        smallA, small_hitsA = self.pinhole_bundle(A, x_opt, hole_half_2,
                                                  x_screen_pinhole,
                                                  n=5, opacity=0.40)
        smallB, small_hitsB = self.pinhole_bundle(B, x_opt, hole_half_2,
                                                  x_screen_pinhole,
                                                  n=5, opacity=0.40)
        smallPatchA = self.patch_from_hits(small_hitsA, x_screen_pinhole)
        smallPatchB = self.patch_from_hits(small_hitsB, x_screen_pinhole)
        blur2 = self.make_blurred_flower(
            object_flower=flower,
            center=inset_center + DOWN*0.05,
            scale_factor=0.505,
            blur_radius=0.045,
            opacity=0.17
        )

        self.play(Transform(aperture, aperture_small),
                  ReplacementTransform(bundleA, smallA),
                  ReplacementTransform(bundleB, smallB),
                  ReplacementTransform(patchA, smallPatchA),
                  ReplacementTransform(patchB, smallPatchB),
                  ReplacementTransform(blur1, blur2),
                  FadeOut(scattered), FadeOut(scatter_label),
                  run_time=1.5)

        bundleA, bundleB = smallA, smallB
        patchA, patchB = smallPatchA, smallPatchB
        blur1 = blur2
        self.wait(0.8)

        # 3. LENTILLE IDÉALE
        self.play(FadeOut(caption_patch),
                  FadeOut(hole_label), FadeOut(screen_label),
                  FadeOut(bundleA), FadeOut(bundleB),
                  FadeOut(patchA), FadeOut(patchB),
                  FadeOut(aperture), FadeOut(blur1),
                  Transform(title,
                            Text("Lentille idéale : correspondance point à point",
                                 font_size=30).to_edge(UP)))

        lens = self.make_lens(x_opt)
        new_screen = self.make_screen(x_screen_lens)
        self.play(FadeIn(lens), Transform(screen, new_screen), run_time=1.0)

        lens_label = Text("lentille idéale", font_size=21)
        lens_label.next_to(lens, DOWN, buff=0.12)
        self.play(FadeIn(lens_label))

        A_img = np.array([x_screen_lens, gamma_lens*A[1], 0.0])
        B_img = np.array([x_screen_lens, gamma_lens*B[1], 0.0])
        heights = [-1.45, -0.75, 0.0, 0.75, 1.45]

        raysA = self.ideal_lens_bundle(A, x_opt, A_img, heights)
        raysB = self.ideal_lens_bundle(B, x_opt, B_img, heights)
        self.play(Create(raysA), run_time=1.3)
        self.play(Create(raysB), run_time=1.3)

        imgdots = VGroup(
            Dot(A_img, radius=0.060),
            Dot(B_img, radius=0.060)
        )
        imglabels = VGroup(Text("A′", font_size=22).next_to(A_img, RIGHT, buff=0.08),
                           Text("B′", font_size=22).next_to(B_img, RIGHT, buff=0.08))
        self.play(FadeIn(imgdots), FadeIn(imglabels))

        caption_image = Text("A donne un point A′ : image stigmatique",
                             font_size=22).to_edge(DOWN)
        self.play(FadeIn(caption_image))

        # Inset : reconstruction nette, point par point, de l'image renversée.
        sharp_flower = self.make_sharp_flower(
            object_flower=flower,
            center=inset_center + DOWN*0.05,
            scale_factor=0.505
        )
        # Une seule construction géométrique : aucune copie décalée,
        # aucune tache résiduelle. Dans le modèle idéal, chaque point
        # objet possède un unique point image.
        # Quelques points apparaissent d'abord pour matérialiser
        # la correspondance point -> point, puis l'image entière apparaît
        # sans aucune copie décalée ni flou résiduel.
        sample_pts = VGroup(
            Dot(inset_center + np.array([-0.18,  0.34, 0]), radius=0.035),
            Dot(inset_center + np.array([ 0.20,  0.18, 0]), radius=0.035),
            Dot(inset_center + np.array([ 0.00, -0.10, 0]), radius=0.035),
            Dot(inset_center + np.array([-0.10, -0.52, 0]), radius=0.035),
            Dot(inset_center + np.array([ 0.16, -0.74, 0]), radius=0.035),
        )
        self.play(LaggedStart(*[FadeIn(p) for p in sample_pts],
                              lag_ratio=0.18),
                  run_time=1.0)
        self.play(FadeIn(sharp_flower), FadeOut(sample_pts), run_time=0.8)
        self.wait(0.5)

        # Les rayons venant de la lentille S'ARRÊTENT en A' et B' sur l'écran.
        # Chaque point éclairé de l'écran diffuse ensuite ; la pupille sélectionne un pinceau divergent.
        lens_scatter_label = Text("chaque point de l'image devient un point-objet pour l'œil",
                                  font_size=17)
        lens_scatter_label.next_to(eye, DOWN, buff=0.16).shift(LEFT*0.70)
        # A' et B' sont maintenant des points matériels lumineux
        # de l'écran-calque. Pour l'œil, chacun joue le rôle d'un
        # nouveau point-objet et envoie un PINCEAU dans la pupille.
        lens_scattered_A = self.divergent_bundle_to_pupil(
            A_img, eye, n=7, opacity=0.74, width=1.35
        )
        lens_scattered_B = self.divergent_bundle_to_pupil(
            B_img, eye, n=7, opacity=0.74, width=1.35
        )

        self.play(FadeIn(lens_scatter_label))
        self.play(Create(lens_scattered_A), run_time=0.55)
        self.play(Create(lens_scattered_B), run_time=0.55)

        final = Text("sténopé : point → tache   |   lentille idéale : point → point",
                     font_size=21).to_edge(DOWN)
        self.play(FadeOut(caption_image), FadeIn(final),
                  Transform(title,
                            Text("De la figure à l'image",
                                 font_size=32).to_edge(UP)))
        self.wait(2.0)
