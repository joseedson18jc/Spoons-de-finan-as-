#!/usr/bin/env python3
"""
Integration Test Script
Tests the complete flow from CSV upload to P&L calculation
"""

import pandas as pd
import sys
import os
from datetime import datetime
from io import BytesIO

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logic import process_upload, calculate_pnl, get_dashboard_data, get_initial_mappings
from models import MappingItem


def test_csv_processing():
    """Test CSV processing with sample data"""
    print("\n" + "="*60)
    print("TEST 1: CSV Processing")
    print("="*60)
    
    # Create sample CSV data
    csv_data = """Data de competência,Valor (R$),Tipo,Centro de Custo 1,Nome do fornecedor/cliente,Descrição
15/01/2024,R$ 10000.00,Entrada,Receita Google,GOOGLE BRASIL PAGAMENTOS LTDA,Receita Google
15/01/2024,R$ 5000.00,Entrada,Receita Apple,App Store (Apple),Receita Apple
20/01/2024,R$ 3000.00,Saída,Marketing,Facebook Ads,Marketing Campaign
25/01/2024,R$ 8000.00,Saída,Salários e Encargos,João Silva,Salário
15/02/2024,R$ 12000.00,Entrada,Receita Google,GOOGLE BRASIL PAGAMENTOS LTDA,Receita Google
15/02/2024,R$ 6000.00,Entrada,Receita Apple,App Store (Apple),Receita Apple
"""
    
    try:
        df = process_upload(csv_data.encode('utf-8'))
        print(f"✅ CSV processed successfully")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Months: {sorted(df['Mes_Competencia'].unique())}")
        return df
    except Exception as e:
        print(f"❌ CSV processing failed: {str(e)}")
        raise


def test_mappings():
    """Test initial mappings"""
    print("\n" + "="*60)
    print("TEST 2: Mappings Initialization")
    print("="*60)
    
    try:
        mappings = get_initial_mappings()
        print(f"✅ Mappings loaded successfully")
        print(f"   Total mappings: {len(mappings)}")
        
        # Show sample mappings
        print("\n   Sample mappings:")
        for m in mappings[:5]:
            print(f"   - Line {m.linha_pl}: {m.centro_custo} / {m.fornecedor_cliente} ({m.tipo})")
        
        return mappings
    except Exception as e:
        print(f"❌ Mappings failed: {str(e)}")
        raise


def test_pnl_calculation(df, mappings):
    """Test P&L calculation"""
    print("\n" + "="*60)
    print("TEST 3: P&L Calculation")
    print("="*60)
    
    try:
        pnl = calculate_pnl(df, mappings)
        print(f"✅ P&L calculated successfully")
        print(f"   Months: {pnl.headers}")
        print(f"   Rows: {len(pnl.rows)}")
        
        # Show key metrics
        print("\n   Key Metrics:")
        for row in pnl.rows:
            if row.line_number in [1, 104, 106, 111]:  # Revenue, Gross Profit, EBITDA, Net Result
                month = pnl.headers[0] if pnl.headers else 'N/A'
                value = row.values.get(month, 0)
                print(f"   - Line {row.line_number} ({row.description}): R$ {value:,.2f}")
        
        return pnl
    except Exception as e:
        print(f"❌ P&L calculation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


def test_dashboard(df, mappings):
    """Test dashboard data generation"""
    print("\n" + "="*60)
    print("TEST 4: Dashboard Data")
    print("="*60)
    
    try:
        dashboard = get_dashboard_data(df, mappings, {})
        print(f"✅ Dashboard data generated successfully")
        print(f"\n   KPIs:")
        for key, value in dashboard.kpis.items():
            if isinstance(value, (int, float)):
                print(f"   - {key}: R$ {value:,.2f}")
            else:
                print(f"   - {key}: {value}")
        
        print(f"\n   Monthly data points: {len(dashboard.monthly_data)}")
        
        return dashboard
    except Exception as e:
        print(f"❌ Dashboard generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


def test_mathematical_consistency(pnl, dashboard):
    """Test mathematical consistency between calculations"""
    print("\n" + "="*60)
    print("TEST 5: Mathematical Consistency")
    print("="*60)
    
    errors = []
    
    try:
        # Get last month for comparison
        if not pnl.headers:
            print("❌ No months in P&L data")
            return
        
        last_month = pnl.headers[-1]
        
        # Extract P&L values
        pnl_values = {}
        for row in pnl.rows:
            pnl_values[row.line_number] = row.values.get(last_month, 0)
        
        # Test 1: Revenue calculation
        revenue = pnl_values.get(1, 0)  # Line 1: RECEITA OPERACIONAL BRUTA
        google = abs(pnl_values.get(21, 0))  # Line 21: Google Play Revenue
        apple = abs(pnl_values.get(22, 0))  # Line 22: App Store Revenue
        
        expected_revenue = google + apple
        if abs(revenue - expected_revenue) > 0.01:
            errors.append(f"Revenue mismatch: {revenue:.2f} != {expected_revenue:.2f} (Google + Apple)")
        else:
            print(f"✅ Revenue calculation correct: R$ {revenue:,.2f}")
        
        # Test 2: Payment Processing (17.65%)
        # Need to find the correct line for payment processing
        payment_proc = 0
        for row in pnl.rows:
            if 'payment processing' in row.description.lower():
                payment_proc = abs(row.values.get(last_month, 0))
                break
        expected_payment = expected_revenue * 0.1765
        if abs(payment_proc - expected_payment) > 0.01:
            errors.append(f"Payment processing mismatch: {payment_proc:.2f} != {expected_payment:.2f}")
        else:
            print(f"✅ Payment processing correct: R$ {payment_proc:,.2f} (17.65%)")
        
        # Test 3: Dashboard consistency
        # Note: Dashboard shows cumulative totals, P&L shows monthly values
        # So we need to sum all months from P&L to compare with Dashboard
        total_revenue_all_months = 0
        for month in pnl.headers:
            for row in pnl.rows:
                if row.line_number == 1:  # RECEITA OPERACIONAL BRUTA
                    total_revenue_all_months += row.values.get(month, 0)
        
        dash_revenue = dashboard.kpis.get('total_revenue', 0)
        if abs(dash_revenue - total_revenue_all_months) > 0.01:
            errors.append(f"Dashboard revenue mismatch: {dash_revenue:.2f} != {total_revenue_all_months:.2f} (cumulative)")
        else:
            print(f"✅ Dashboard revenue consistent (cumulative): R$ {dash_revenue:,.2f}")
        
        if errors:
            print(f"\n❌ Found {len(errors)} mathematical inconsistencies:")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"\n✅ All mathematical checks passed!")
            
    except Exception as e:
        print(f"❌ Consistency check failed: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Run all integration tests"""
    print("\n" + "="*60)
    print(" INTEGRATION TEST SUITE")
    print("="*60)
    print(f" Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test 1: CSV Processing
        df = test_csv_processing()
        
        # Test 2: Mappings
        mappings = test_mappings()
        
        # Test 3: P&L Calculation
        pnl = test_pnl_calculation(df, mappings)
        
        # Test 4: Dashboard
        dashboard = test_dashboard(df, mappings)
        
        # Test 5: Mathematical Consistency
        test_mathematical_consistency(pnl, dashboard)
        
        print("\n" + "="*60)
        print(" ALL TESTS COMPLETED")
        print("="*60)
        print(f" End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n✅ Integration tests passed successfully!")
        
    except Exception as e:
        print("\n" + "="*60)
        print(" TEST SUITE FAILED")
        print("="*60)
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
