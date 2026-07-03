# ======================================================================
# PROYECTO FINAL INVESTIGACIÓN DE OPERACIONES - PANADERÍA "EL TRIGAL"
# OPTIMIZACIÓN DE LA PRODUCCIÓN SEMANAL (LINEAL Y ENTERA MIXTA)
# ======================================================================

import pulp

print("======================================================================")
print("  PROYECTO INVESTIGACIÓN DE OPERACIONES - PANADERÍA 'EL TRIGAL'       ")
print("======================================================================")

# ======================================================================
# FASE 1: RESOLUCIÓN DEL MODELO LINEAL CONTINUO (Para Dualidad y Simplex)
# ======================================================================

# 1. Instanciar el problema de maximización
prob_lp = pulp.LpProblem("Panaderia_El_Trigal_LP", pulp.LpMaximize)

# 2. Definir Variables de Decisión Continuas (Permiten análisis marginal / Precios Sombra)
x1 = pulp.LpVariable('Pan_Frances', lowBound=400, upBound=1200, cat='Continuous')
x2 = pulp.LpVariable('Pan_Molde', lowBound=150, upBound=700, cat='Continuous')
x3 = pulp.LpVariable('Pan_Integral', lowBound=100, upBound=500, cat='Continuous')
x4 = pulp.LpVariable('Pan_Dulce', lowBound=200, upBound=800, cat='Continuous')
x5 = pulp.LpVariable('Croissant', lowBound=80, upBound=400, cat='Continuous')

# 3. Declaración de la Función Objetivo (Utilidad en USD)
prob_lp += 0.60*x1 + 1.20*x2 + 1.10*x3 + 0.95*x4 + 1.50*x5, "Utilidad_Total"

# 4. Vinculación de Restricciones Técnicas y Tecnológicas de Insumos
prob_lp += 0.40*x1 + 0.55*x2 + 0.50*x3 + 0.35*x4 + 0.28*x5 <= 900, "Harina"
prob_lp += 0.010*x1 + 0.012*x2 + 0.011*x3 + 0.008*x4 + 0.007*x5 <= 25, "Levadura"
prob_lp += 0.00*x1 + 0.03*x2 + 0.02*x3 + 0.06*x4 + 0.04*x5 <= 150, "Azucar"
prob_lp += 0.00*x1 + 0.02*x2 + 0.01*x3 + 0.04*x4 + 0.06*x5 <= 120, "Mantequilla"
prob_lp += 0.12*x1 + 0.18*x2 + 0.16*x3 + 0.15*x4 + 0.20*x5 <= 320, "Mano_de_Obra"
prob_lp += 0.08*x1 + 0.10*x2 + 0.09*x3 + 0.09*x4 + 0.12*x5 <= 180, "Horno"

# 5. Ejecución del Solver Lineal (Por defecto, silencioso)
prob_lp.solve(pulp.PULP_CBC_CMD(msg=False))

# --- Impresión de Resultados del Modelo Continuo ---
print("\n>>> 1. RESULTADOS GENERALES DE LA OPTIMIZACIÓN CONTINUA <<<")
print(f"Estado de Convergencia: {pulp.LpStatus[prob_lp.status]}")
print(f"Utilidad Máxima Teórica (Z*): ${pulp.value(prob_lp.objective):,.2f} USD semanales")

print("\nPlan Físico Matemático Recomendado:")
for v in prob_lp.variables():
    print(f"  - {v.name}: {v.varValue:.2f} unidades")

print("\n>>> 2. ANÁLISIS DE DUALIDAD, HOLGURAS Y PRECIOS SOMBRA <<<")
for name, c in prob_lp.constraints.items():
    print(f"  - Restricción [{name}]:")
    print(f"    Holgura (Inventario Restante) = {c.slack:.2f}")
    print(f"    Precio Sombra (Valor Marginal) = ${c.pi:.4f} USD por unidad de recurso")


print("\n" + "="*70)
# ======================================================================
# FASE 2: RESOLUCIÓN DEL MODELO DE PROGRAMACIÓN ENTERA MIXTA (MILP)
# ======================================================================

# 1. Instanciar el problema entero
prob_ilp = pulp.LpProblem("Panaderia_El_Trigal_ILP", pulp.LpMaximize)

# 2. Definir Variables de Decisión como Enteras (cat='Integer')
x1_i = pulp.LpVariable('Pan_Frances', lowBound=400, upBound=1200, cat='Integer')
x2_i = pulp.LpVariable('Pan_Molde', lowBound=150, upBound=700, cat='Integer')
x3_i = pulp.LpVariable('Pan_Integral', lowBound=100, upBound=500, cat='Integer')
x4_i = pulp.LpVariable('Pan_Dulce', lowBound=200, upBound=800, cat='Integer')
x5_i = pulp.LpVariable('Croissant', lowBound=80, upBound=400, cat='Integer')

# 3. Función Objetivo
prob_ilp += 0.60*x1_i + 1.20*x2_i + 1.10*x3_i + 0.95*x4_i + 1.50*x5_i, "Utilidad_Total"

# 4. Restricciones
prob_ilp += 0.40*x1_i + 0.55*x2_i + 0.50*x3_i + 0.35*x4_i + 0.28*x5_i <= 900, "Harina"
prob_ilp += 0.010*x1_i + 0.012*x2_i + 0.011*x3_i + 0.008*x4_i + 0.007*x5_i <= 25, "Levadura"
prob_ilp += 0.00*x1_i + 0.03*x2_i + 0.02*x3_i + 0.06*x4_i + 0.04*x5_i <= 150, "Azucar"
prob_ilp += 0.00*x1_i + 0.02*x2_i + 0.01*x3_i + 0.04*x4_i + 0.06*x5_i <= 120, "Mantequilla"
prob_ilp += 0.12*x1_i + 0.18*x2_i + 0.16*x3_i + 0.15*x4_i + 0.20*x5_i <= 320, "Mano_de_Obra"
prob_ilp += 0.08*x1_i + 0.10*x2_i + 0.09*x3_i + 0.09*x4_i + 0.12*x5_i <= 180, "Horno"

# 5. Resolver usando algoritmo de Ramificación y Acotamiento (Branch & Bound)
prob_ilp.solve(pulp.PULP_CBC_CMD(msg=False))

# --- Impresión de Resultados del Modelo Entero ---
print(">>> 3. ANÁLISIS DEL MODELO REAL ACUMULADO (PROGRAMACIÓN ENTERA) <<<")
print(f"Estado del Solver: {pulp.LpStatus[prob_ilp.status]}")
print(f"Utilidad Máxima Entera Realizable (Z_int): ${pulp.value(prob_ilp.objective):,.2f} USD semanales")

print("\nPlan Técnico de Producción de Piezas Enteras:")
for v in prob_ilp.variables():
    print(f"  - {v.name}: {int(v.varValue)} unidades exactas")
print("======================================================================")