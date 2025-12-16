# UMatch Financial Control System (Versão Final Consolidada)

Este repositório contém a versão auditada e corrigida do sistema financeiro UMatch.

## 📁 Estrutura do Projeto

O código-fonte principal está localizado na pasta `financial-control-app-main/`:

- **Backend**: `financial-control-app-main/backend/` (Python/FastAPI)
- **Frontend**: `financial-control-app-main/frontend/` (React/Vite)

> **Nota**: Arquivos duplicados que estavam na raiz foram movidos para `_backup_root/` para evitar confusão. Utilize sempre os arquivos dentro de `financial-control-app-main`.

## ✅ Correções e Auditoria (Dezembro 2025)

### 1. Lógica Financeira (Backend)
- **Lucro Bruto**: Fórmula corrigida para `Receita Total - Payment Processing - COGS`.
- **Rendimentos**: Agora incluídos corretamente na Receita Operacional.
- **Validação Matemática**: Implementada verificação automática com tolerância de R$ 0.01.

### 2. Interface (Frontend)
- **Alertas**: Novos alertas visuais no DRE quando há discrepâncias matemáticas.
- **Tradução**: Corrigido bug de persistência do idioma (PT/EN).
- **Gráficos**: Validados para refletir os dados corretos do backend.

## 🚀 Como Rodar

### Backend
```bash
cd financial-control-app-main/backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd financial-control-app-main/frontend
npm install
npm run dev
```

## 📊 Status da Auditoria
- **Integridade**: Arquivos verificados e completos.
- **Matemática**: Fórmulas validadas e testadas.
- **Limpeza**: Arquivos temporários e duplicatas removidos.

---
*Versão: 1.0.1 (Consolidada)*
