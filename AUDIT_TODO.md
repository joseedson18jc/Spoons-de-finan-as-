# Auditoria Completa do Sistema Financeiro

## 1. Backend (Python)
- [ ] `logic.py`: Verificar se está completo e sem truncamentos
- [ ] `logic.py`: Validar fórmula do Lucro Bruto (Gross Profit)
- [ ] `logic.py`: Validar fórmula do EBITDA
- [ ] `logic.py`: Validar tratamento de sinais (receitas +, despesas -)
- [ ] `models.py`: Verificar integridade dos modelos Pydantic
- [ ] `main.py`: Verificar endpoints e tratamento de erros
- [ ] `validation.py`: Confirmar lógica de alertas matemáticos

## 2. Frontend (React/TypeScript)
- [ ] `PnLTable.tsx`: Verificar renderização e alertas
- [ ] `Dashboard.tsx`: Verificar gráficos e KPIs
- [ ] `App.tsx`: Verificar roteamento e gestão de estado (idioma/auth)
- [ ] `api.ts`: Verificar configuração do Axios
- [ ] Verificar se há arquivos truncados ou com sintaxe inválida

## 3. Dados e Cálculos
- [ ] Verificar mapeamento de categorias (CSV -> DRE)
- [ ] Confirmar cálculo de Payment Processing (17.65%)
- [ ] Confirmar inclusão de Rendimentos na Receita Operacional

## 4. Limpeza
- [ ] Remover código comentado obsoleto
- [ ] Remover arquivos temporários ou de backup
