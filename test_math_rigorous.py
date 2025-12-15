#!/usr/bin/env python3
"""
TESTE MATEMÁTICO RIGOROSO
Valida TODAS as fórmulas financeiras linha por linha
"""

import pandas as pd
import sys
from io import BytesIO

sys.path.insert(0, '/home/claude/financial-control-app-main/backend')

from logic import process_upload, calculate_pnl, get_dashboard_data, get_initial_mappings

def test_formula_validation():
    """Valida matematicamente TODAS as fórmulas"""
    
    print("\n" + "="*70)
    print("VALIDAÇÃO MATEMÁTICA RIGOROSA DE TODAS AS FÓRMULAS")
    print("="*70)
    
    # Dados de teste com valores conhecidos
    csv_data = """Data de competência,Valor (R$),Tipo,Centro de Custo 1,Nome do fornecedor/cliente,Descrição
15/01/2024,R$ 100000.00,Entrada,Receita Google,GOOGLE BRASIL PAGAMENTOS LTDA,Receita Google
15/01/2024,R$ 50000.00,Entrada,Receita Apple,App Store (Apple),Receita Apple
20/01/2024,R$ 10000.00,Saída,Marketing & Growth Expenses,MGA MARKETING LTDA,Marketing
25/01/2024,R$ 20000.00,Saída,Wages Expenses,Diversos,Salários
28/01/2024,R$ 5000.00,Saída,Tech Support & Services,Adobe,Tech Support
30/01/2024,R$ 2000.00,Saída,Web Services Expenses,AWS,COGS
31/01/2024,R$ 3000.00,Saída,Legal & Accounting Expenses,BHUB.AI,Other Expenses
"""
    
    df = process_upload(csv_data.encode('utf-8'))
    mappings = get_initial_mappings()
    pnl = calculate_pnl(df, mappings, {})
    
    # Extrair valores do P&L
    month = pnl.headers[0]
    values = {}
    
    for row in pnl.rows:
        values[row.line_number] = row.values.get(month, 0)
    
    print(f"\n📅 Mês analisado: {month}\n")
    
    errors = []
    
    # ========================================================================
    # TESTE 1: RECEITA TOTAL
    # ========================================================================
    print("TESTE 1: Receita Total")
    print("-" * 70)
    
    google_rev = abs(values.get(21, 0))  # Google Play Revenue
    apple_rev = abs(values.get(22, 0))   # App Store Revenue
    invest_income = abs(values.get(3, 0))  # Rendimentos
    
    expected_total_revenue = google_rev + apple_rev + invest_income
    actual_total_revenue = values.get(1, 0)  # RECEITA OPERACIONAL BRUTA
    
    print(f"Google Revenue:        R$ {google_rev:>12,.2f}")
    print(f"Apple Revenue:         R$ {apple_rev:>12,.2f}")
    print(f"Investment Income:     R$ {invest_income:>12,.2f}")
    print(f"{'─'*50}")
    print(f"Expected Total:        R$ {expected_total_revenue:>12,.2f}")
    print(f"Actual Total:          R$ {actual_total_revenue:>12,.2f}")
    
    if abs(actual_total_revenue - expected_total_revenue) < 0.01:
        print("✅ FÓRMULA CORRETA\n")
    else:
        error_msg = f"Receita Total: Esperado={expected_total_revenue:.2f}, Real={actual_total_revenue:.2f}"
        errors.append(error_msg)
        print(f"❌ ERRO: Diferença de R$ {abs(actual_total_revenue - expected_total_revenue):.2f}\n")
    
    # ========================================================================
    # TESTE 2: PAYMENT PROCESSING (17.65%)
    # ========================================================================
    print("TESTE 2: Payment Processing (17.65%)")
    print("-" * 70)
    
    revenue_no_invest = google_rev + apple_rev
    expected_payment_proc = revenue_no_invest * 0.1765
    
    # Payment processing é negativo no P&L
    actual_payment_proc = abs(values.get(5, 0))  # Payment Processing (17.65%)
    
    print(f"Revenue (no invest):   R$ {revenue_no_invest:>12,.2f}")
    print(f"Rate:                       {17.65:>12.2f}%")
    print(f"{'─'*50}")
    print(f"Expected Payment Proc: R$ {expected_payment_proc:>12,.2f}")
    print(f"Actual Payment Proc:   R$ {actual_payment_proc:>12,.2f}")
    
    if abs(actual_payment_proc - expected_payment_proc) < 0.01:
        print("✅ FÓRMULA CORRETA\n")
    else:
        error_msg = f"Payment Processing: Esperado={expected_payment_proc:.2f}, Real={actual_payment_proc:.2f}"
        errors.append(error_msg)
        print(f"❌ ERRO: Diferença de R$ {abs(actual_payment_proc - expected_payment_proc):.2f}\n")
    
    # ========================================================================
    # TESTE 3: COGS
    # ========================================================================
    print("TESTE 3: COGS (Cost of Goods Sold)")
    print("-" * 70)
    
    # COGS = 2000 (AWS)
    expected_cogs = 2000.00
    actual_cogs = abs(values.get(6, 0))  # COGS (Web Services)
    
    print(f"Expected COGS:         R$ {expected_cogs:>12,.2f}")
    print(f"Actual COGS:           R$ {actual_cogs:>12,.2f}")
    
    if abs(actual_cogs - expected_cogs) < 0.01:
        print("✅ FÓRMULA CORRETA\n")
    else:
        error_msg = f"COGS: Esperado={expected_cogs:.2f}, Real={actual_cogs:.2f}"
        errors.append(error_msg)
        print(f"❌ ERRO: Diferença de R$ {abs(actual_cogs - expected_cogs):.2f}\n")
    
    # ========================================================================
    # TESTE 4: LUCRO BRUTO
    # ========================================================================
    print("TESTE 4: Lucro Bruto")
    print("-" * 70)
    
    expected_gross_profit = expected_total_revenue - expected_payment_proc - expected_cogs
    actual_gross_profit = values.get(7, 0)  # (=) LUCRO BRUTO
    
    print(f"Total Revenue:         R$ {expected_total_revenue:>12,.2f}")
    print(f"- Payment Processing:  R$ {expected_payment_proc:>12,.2f}")
    print(f"- COGS:                R$ {expected_cogs:>12,.2f}")
    print(f"{'─'*50}")
    print(f"Expected Gross Profit: R$ {expected_gross_profit:>12,.2f}")
    print(f"Actual Gross Profit:   R$ {actual_gross_profit:>12,.2f}")
    
    if abs(actual_gross_profit - expected_gross_profit) < 0.01:
        print("✅ FÓRMULA CORRETA\n")
    else:
        error_msg = f"Lucro Bruto: Esperado={expected_gross_profit:.2f}, Real={actual_gross_profit:.2f}"
        errors.append(error_msg)
        print(f"❌ ERRO: Diferença de R$ {abs(actual_gross_profit - expected_gross_profit):.2f}\n")
    
    # ========================================================================
    # TESTE 5: OPEX (Despesas Operacionais)
    # ========================================================================
    print("TESTE 5: Despesas Operacionais (OpEx)")
    print("-" * 70)
    
    marketing = 10000.00
    wages = 20000.00
    tech_support = 5000.00
    other_expenses = 3000.00
    
    expected_total_opex = marketing + wages + tech_support + other_expenses
    
    actual_marketing = abs(values.get(9, 0))
    actual_wages = abs(values.get(10, 0))
    actual_tech = abs(values.get(11, 0))
    actual_other = abs(values.get(12, 0))
    actual_total_opex = actual_marketing + actual_wages + actual_tech + actual_other
    
    print(f"Marketing:             R$ {marketing:>12,.2f} (Esperado)")
    print(f"                       R$ {actual_marketing:>12,.2f} (Real)")
    print(f"Wages:                 R$ {wages:>12,.2f} (Esperado)")
    print(f"                       R$ {actual_wages:>12,.2f} (Real)")
    print(f"Tech Support:          R$ {tech_support:>12,.2f} (Esperado)")
    print(f"                       R$ {actual_tech:>12,.2f} (Real)")
    print(f"Other Expenses:        R$ {other_expenses:>12,.2f} (Esperado)")
    print(f"                       R$ {actual_other:>12,.2f} (Real)")
    print(f"{'─'*50}")
    print(f"Expected Total OpEx:   R$ {expected_total_opex:>12,.2f}")
    print(f"Actual Total OpEx:     R$ {actual_total_opex:>12,.2f}")
    
    if abs(actual_total_opex - expected_total_opex) < 0.01:
        print("✅ FÓRMULA CORRETA\n")
    else:
        error_msg = f"OpEx: Esperado={expected_total_opex:.2f}, Real={actual_total_opex:.2f}"
        errors.append(error_msg)
        print(f"❌ ERRO: Diferença de R$ {abs(actual_total_opex - expected_total_opex):.2f}\n")
    
    # ========================================================================
    # TESTE 6: EBITDA
    # ========================================================================
    print("TESTE 6: EBITDA")
    print("-" * 70)
    
    expected_ebitda = expected_gross_profit - expected_total_opex
    actual_ebitda = values.get(13, 0)  # (=) EBITDA
    
    print(f"Gross Profit:          R$ {expected_gross_profit:>12,.2f}")
    print(f"- Total OpEx:          R$ {expected_total_opex:>12,.2f}")
    print(f"{'─'*50}")
    print(f"Expected EBITDA:       R$ {expected_ebitda:>12,.2f}")
    print(f"Actual EBITDA:         R$ {actual_ebitda:>12,.2f}")
    
    if abs(actual_ebitda - expected_ebitda) < 0.01:
        print("✅ FÓRMULA CORRETA\n")
    else:
        error_msg = f"EBITDA: Esperado={expected_ebitda:.2f}, Real={actual_ebitda:.2f}"
        errors.append(error_msg)
        print(f"❌ ERRO: Diferença de R$ {abs(actual_ebitda - expected_ebitda):.2f}\n")
    
    # ========================================================================
    # TESTE 7: RESULTADO LÍQUIDO
    # ========================================================================
    print("TESTE 7: Resultado Líquido")
    print("-" * 70)
    
    expected_net_result = expected_ebitda
    actual_net_result = values.get(16, 0)  # (=) RESULTADO LÍQUIDO
    
    print(f"Expected Net Result:   R$ {expected_net_result:>12,.2f}")
    print(f"Actual Net Result:     R$ {actual_net_result:>12,.2f}")
    
    if abs(actual_net_result - expected_net_result) < 0.01:
        print("✅ FÓRMULA CORRETA\n")
    else:
        error_msg = f"Resultado Líquido: Esperado={expected_net_result:.2f}, Real={actual_net_result:.2f}"
        errors.append(error_msg)
        print(f"❌ ERRO: Diferença de R$ {abs(actual_net_result - expected_net_result):.2f}\n")
    
    # ========================================================================
    # TESTE 8: MARGENS
    # ========================================================================
    print("TESTE 8: Margens")
    print("-" * 70)
    
    expected_ebitda_margin = (expected_ebitda / expected_total_revenue) * 100
    expected_gross_margin = (expected_gross_profit / expected_total_revenue) * 100
    
    actual_ebitda_margin = values.get(14, 0)  # Margem EBITDA %
    actual_gross_margin = values.get(15, 0)  # Margem Bruta %
    
    print(f"Expected EBITDA Margin:      {expected_ebitda_margin:>8.2f}%")
    print(f"Actual EBITDA Margin:        {actual_ebitda_margin:>8.2f}%")
    print(f"Expected Gross Margin:       {expected_gross_margin:>8.2f}%")
    print(f"Actual Gross Margin:         {actual_gross_margin:>8.2f}%")
    
    if abs(actual_ebitda_margin - expected_ebitda_margin) < 0.01 and \
       abs(actual_gross_margin - expected_gross_margin) < 0.01:
        print("✅ FÓRMULAS CORRETAS\n")
    else:
        if abs(actual_ebitda_margin - expected_ebitda_margin) >= 0.01:
            error_msg = f"Margem EBITDA: Esperado={expected_ebitda_margin:.2f}%, Real={actual_ebitda_margin:.2f}%"
            errors.append(error_msg)
        if abs(actual_gross_margin - expected_gross_margin) >= 0.01:
            error_msg = f"Margem Bruta: Esperado={expected_gross_margin:.2f}%, Real={actual_gross_margin:.2f}%"
            errors.append(error_msg)
        print("❌ ERRO NAS MARGENS\n")
    
    # ========================================================================
    # TESTE 9: CONSISTÊNCIA DASHBOARD
    # ========================================================================
    print("TESTE 9: Consistência do Dashboard")
    print("-" * 70)
    
    dashboard = get_dashboard_data(df, mappings, {})
    
    dash_revenue = dashboard.kpis['total_revenue']
    dash_ebitda = dashboard.kpis['ebitda']
    dash_net = dashboard.kpis['net_result']
    
    print(f"Dashboard Revenue:     R$ {dash_revenue:>12,.2f}")
    print(f"P&L Revenue:           R$ {actual_total_revenue:>12,.2f}")
    print(f"Dashboard EBITDA:      R$ {dash_ebitda:>12,.2f}")
    print(f"P&L EBITDA:            R$ {actual_ebitda:>12,.2f}")
    print(f"Dashboard Net Result:  R$ {dash_net:>12,.2f}")
    print(f"P&L Net Result:        R$ {actual_net_result:>12,.2f}")
    
    if abs(dash_revenue - actual_total_revenue) < 0.01 and \
       abs(dash_ebitda - actual_ebitda) < 0.01 and \
       abs(dash_net - actual_net_result) < 0.01:
        print("✅ DASHBOARD CONSISTENTE COM P&L\n")
    else:
        if abs(dash_revenue - actual_total_revenue) >= 0.01:
            error_msg = f"Dashboard Revenue inconsistente"
            errors.append(error_msg)
        if abs(dash_ebitda - actual_ebitda) >= 0.01:
            error_msg = f"Dashboard EBITDA inconsistente"
            errors.append(error_msg)
        if abs(dash_net - actual_net_result) >= 0.01:
            error_msg = f"Dashboard Net Result inconsistente"
            errors.append(error_msg)
        print("❌ INCONSISTÊNCIA DETECTADA\n")
    
    # ========================================================================
    # RESULTADO FINAL
    # ========================================================================
    print("="*70)
    if len(errors) == 0:
        print("✅ TODAS AS 9 VALIDAÇÕES MATEMÁTICAS PASSARAM COM SUCESSO!")
        print("="*70)
        return True
    else:
        print(f"❌ {len(errors)} ERRO(S) DETECTADO(S):")
        print("="*70)
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")
        print("="*70)
        return False

if __name__ == "__main__":
    success = test_formula_validation()
    sys.exit(0 if success else 1)
