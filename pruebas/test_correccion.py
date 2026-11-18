"""
Pruebas de corrección (R2). Ejecutar:  python -m unittest discover -s pruebas
Una estrategia más rápida pero incorrecta NO es una mejora.
"""
import unittest

from src import estrategia_b, estrategia_c, linea_base


ESTRATEGIAS = {
    "B_invariantes": estrategia_b,
    "C_formula_cache": estrategia_c,
}


class TestCorreccion(unittest.TestCase):
    def test_linea_base_ejecuta(self):
        d = linea_base.preparar(50)
        self.assertIsNotNone(linea_base.ejecutar(d))

    def test_estrategias_equivalentes_a_linea_base(self):
        # Varios tamaños ejercitan entradas pequeñas y lotes con repeticiones
        # de las combinaciones tasa–plazo del portafolio.
        for n in (1, 50, 250):
            with self.subTest(n=n):
                solicitudes = linea_base.preparar(n, semilla=42)
                esperado = linea_base.ejecutar(solicitudes)
                for nombre, modulo in ESTRATEGIAS.items():
                    with self.subTest(estrategia=nombre):
                        obtenido = modulo.ejecutar(solicitudes)
                        self.assertLessEqual(
                            abs(obtenido - esperado),
                            0.01,
                            f"{nombre}: {obtenido} COP vs {esperado} COP para n={n}",
                        )

    def test_linea_base_lista_vacia(self):
        self.assertEqual(linea_base.ejecutar([]), 0.0)

    def test_datos_reproducibles_con_semilla(self):
        self.assertEqual(linea_base.preparar(100, semilla=17), linea_base.preparar(100, semilla=17))


if __name__ == "__main__":
    unittest.main()
