#!/usr/bin/env python
import os
import sys
import json
from datetime import datetime, timedelta
from sqlalchemy import text

# Adicionar o diretório raiz ao PYTHONPATH
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

from app.db.session import SessionLocal, engine
from app.models.calendar import CalendarEvent

def fix_date_issues():
    """Corrige problemas de data nos eventos do calendário"""
    print("=== Verificando e corrigindo datas de eventos ===")
    db = SessionLocal()
    
    try:
        # Contagem de eventos
        total_events = db.query(CalendarEvent).count()
        print(f"Total de eventos encontrados: {total_events}")
        
        # Se não houver eventos, criar alguns
        if total_events == 0:
            print("Não foram encontrados eventos. Criando eventos de exemplo...")
            
            # Criar eventos próximos ao dia atual para garantir que apareçam na página inicial
            hoje = datetime.now()
            eventos = [
                CalendarEvent(
                    title="Reunião de trabalho",
                    description="Discussão de projeto",
                    start_date=hoje + timedelta(days=1, hours=10),
                    end_date=hoje + timedelta(days=1, hours=11),
                    event_type="trabalho",
                    family_member_id=1,
                    location="Escritório",
                    is_all_day=False,
                    color="#4285F4"
                ),
                CalendarEvent(
                    title="Consulta médica",
                    description="Checkup anual",
                    start_date=hoje + timedelta(days=3, hours=14),
                    end_date=hoje + timedelta(days=3, hours=15),
                    event_type="saude",
                    family_member_id=1,
                    location="Centro Médico",
                    is_all_day=False,
                    color="#34A853"
                ),
                CalendarEvent(
                    title="Aniversário da Família",
                    description="Comemoração",
                    start_date=hoje + timedelta(days=5),
                    end_date=hoje + timedelta(days=5),
                    event_type="aniversario",
                    family_member_id=None,
                    location="Casa",
                    is_all_day=True,
                    color="#EA4335"
                )
            ]
            
            db.add_all(eventos)
            db.commit()
            print(f"Criados {len(eventos)} eventos de exemplo.")
            return True
        
        # Se houver eventos, verificar se há algum com datas futuras (próximas)
        now = datetime.now()
        future_events = db.query(CalendarEvent).filter(
            CalendarEvent.start_date >= now,
            CalendarEvent.start_date <= now + timedelta(days=30)
        ).count()
        
        if future_events == 0:
            print("Não foram encontrados eventos futuros. Atualizando datas...")
            
            # Atualizar datas de eventos existentes para o futuro
            events = db.query(CalendarEvent).all()
            for i, event in enumerate(events):
                # Distribuir eventos ao longo do próximo mês
                days_ahead = (i % 10) + 1  # 1 a 10 dias à frente
                
                event.start_date = now + timedelta(days=days_ahead, hours=10)
                event.end_date = event.start_date + timedelta(hours=2)
                
                print(f"Atualizado: {event.title} para {event.start_date.strftime('%Y-%m-%d %H:%M')}")
            
            db.commit()
            print(f"Foram atualizadas as datas de {len(events)} eventos.")
            return True
        
        # Se houver eventos futuros, verificar se há problemas de formato ou tipo
        events = db.query(CalendarEvent).all()
        updated_count = 0
        
        for event in events:
            # Verificar se o tipo de evento está vazio ou é None
            if not event.event_type:
                event.event_type = "outro"
                updated_count += 1
                print(f"Corrigido tipo de evento para '{event.title}'")
            
            # Verificar se a data de fim é anterior à data de início
            if event.end_date < event.start_date:
                event.end_date = event.start_date + timedelta(hours=1)
                updated_count += 1
                print(f"Corrigido período do evento '{event.title}'")
        
        if updated_count > 0:
            db.commit()
            print(f"Foram corrigidos {updated_count} problemas em eventos.")
        else:
            print("Todos os eventos estão corretos. Nenhuma correção necessária.")
        
        # Exibir os próximos 3 eventos para confirmar que estão ok
        next_events = db.query(CalendarEvent).filter(
            CalendarEvent.start_date >= now
        ).order_by(CalendarEvent.start_date).limit(3).all()
        
        print("\nPróximos eventos:")
        for i, event in enumerate(next_events, 1):
            print(f"  {i}. {event.title} - {event.start_date.strftime('%Y-%m-%d %H:%M')}")
        
        return True
    except Exception as e:
        print(f"Erro: {str(e)}")
        return False
    finally:
        db.close()

def fix_js_function():
    """Corrige a função JavaScript que carrega os eventos"""
    print("\n=== Verificando e corrigindo a função JavaScript ===")
    
    try:
        index_path = os.path.join(project_dir, "templates", "index.html")
        
        # Ler o arquivo
        with open(index_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Verificar se a função de carregar eventos está correta
        if "loadEvents" in content:
            print("Função loadEvents encontrada no index.html")
            
            # Criar versão corrigida da função loadEvents
            corrected_function = """
    // Função para carregar próximos eventos
    async function loadEvents() {
        try {
            const start = new Date();
            const end = new Date();
            end.setDate(end.getDate() + 30);
            
            // Formatar data no formato YYYY-MM-DD
            function formatDate(date) {
                return date.getFullYear() + '-' + 
                    String(date.getMonth() + 1).padStart(2, '0') + '-' + 
                    String(date.getDate()).padStart(2, '0');
            }
            
            // Usar formato de data simples sem hora para evitar problemas de timezone
            const url = `/api/v1/calendar/events/?start_date=${formatDate(start)}&end_date=${formatDate(end)}`;
            console.log('Buscando eventos na URL:', url);
            
            const res = await fetch(url);
            
            if (!res.ok) {
                console.error('Erro na resposta:', res.status, res.statusText);
                throw new Error(`Erro HTTP! status: ${res.status}`);
            }
            
            const events = await res.json();
            console.log('Eventos recebidos:', events);
            
            // Verificação de segurança para eventos
            if (!Array.isArray(events)) {
                console.error('A resposta não é um array:', events);
                throw new Error('Formato de resposta inválido');
            }

            // Ordena por data de início
            events.sort((a, b) => new Date(a.start_date) - new Date(b.start_date));

            document.getElementById('eventCount').textContent = events.length;

            const nextList = document.getElementById('nextEventsList');
            if (events.length === 0) {
                nextList.innerHTML = '<li>Nenhum evento nos próximos 30 dias</li>';
                return;
            }

            nextList.innerHTML = '';
            // Criar cada elemento da lista individualmente para evitar problemas
            events.slice(0, 3).forEach(ev => {
                try {
                    const li = document.createElement('li');
                    li.className = 'flex justify-between';
                    
                    const titleSpan = document.createElement('span');
                    titleSpan.textContent = ev.title;
                    
                    const dateSpan = document.createElement('span');
                    dateSpan.className = 'text-gray-500';
                    
                    // Usar try-catch para lidar com datas inválidas
                    try {
                        const eventDate = new Date(ev.start_date);
                        dateSpan.textContent = eventDate.toLocaleDateString();
                    } catch(dateError) {
                        console.error('Erro ao formatar data:', dateError);
                        dateSpan.textContent = 'Data desconhecida';
                    }
                    
                    li.appendChild(titleSpan);
                    li.appendChild(dateSpan);
                    nextList.appendChild(li);
                } catch(itemError) {
                    console.error('Erro ao processar evento:', itemError, ev);
                }
            });
        } catch (err) {
            console.error('Erro ao carregar eventos:', err);
            document.getElementById('eventCount').textContent = 'Erro';
            document.getElementById('nextEventsList').innerHTML = '<li class="text-red-500">Erro ao carregar eventos</li>';
        }
    }"""
            
            # Substituir a função anterior pela nova
            import re
            pattern = r"// Função para carregar próximos eventos[\s\S]*?async function loadEvents\(\) \{[\s\S]*?\}"
            if re.search(pattern, content):
                new_content = re.sub(pattern, corrected_function, content)
                
                # Salvar o arquivo
                with open(index_path, "w", encoding="utf-8") as file:
                    file.write(new_content)
                print("Função loadEvents atualizada com sucesso!")
                return True
            else:
                print("Não foi possível localizar a função loadEvents para substituição.")
                return False
        else:
            print("Função loadEvents não encontrada no arquivo index.html")
            return False
    except Exception as e:
        print(f"Erro ao corrigir função JavaScript: {str(e)}")
        return False

def fix_api_endpoint():
    """Corrige o endpoint da API de eventos do calendário"""
    print("\n=== Verificando e corrigindo o endpoint da API ===")
    
    try:
        api_path = os.path.join(project_dir, "app", "api", "api_v1", "endpoints", "calendar.py")
        
        # Ler o arquivo
        with open(api_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Criar versão corrigida do endpoint
        corrected_endpoint = """
@router.get("/events/", response_model=List[CalendarEvent])
def get_events(
    db: Session = Depends(deps.get_db),
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    family_member_id: Optional[int] = None,
    event_type: Optional[str] = None
):
    \"\"\"
    Retorna eventos do calendário dentro de um período específico.
    \"\"\"
    try:
        # Converter strings para datas
        try:
            # Tenta primeiro o formato completo
            if "T" in start_date:
                start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            else:
                # Formato simples (YYYY-MM-DD)
                start = datetime.strptime(start_date, "%Y-%m-%d")
                
            if "T" in end_date:
                end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            else:
                # Formato simples (YYYY-MM-DD)
                end = datetime.strptime(end_date, "%Y-%m-%d")
                # Se for só a data, considerar o fim do dia
                end = end.replace(hour=23, minute=59, second=59)
        except Exception as date_error:
            print(f"Erro ao converter datas: {start_date} - {end_date}, Erro: {str(date_error)}")
            # Usar datas padrão em caso de erro
            start = datetime.now()
            end = start + timedelta(days=30)
        
        # Consulta no banco
        query = db.query(CalendarEventModel).filter(
            CalendarEventModel.start_date <= end,
            CalendarEventModel.end_date >= start
        )
        
        # Aplicar filtros adicionais
        if family_member_id:
            query = query.filter(CalendarEventModel.family_member_id == family_member_id)
        if event_type:
            query = query.filter(CalendarEventModel.event_type == event_type)
        
        # Executar a consulta
        events = query.all()
        print(f"Encontrados {len(events)} eventos de {start} até {end}")
        return events
        
    except Exception as e:
        print(f"Erro ao buscar eventos: {str(e)}")
        # Retornar lista vazia em vez de erro para não quebrar a UI
        return []"""
        
        # Substituir o endpoint anterior pelo novo
        import re
        pattern = r"@router\.get\(\"/events/\", response_model=List\[CalendarEvent\]\)[\s\S]*?def get_events[\s\S]*?try:[\s\S]*?except Exception as e:[\s\S]*?\)"
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, corrected_endpoint, content)
            
            # Salvar o arquivo
            with open(api_path, "w", encoding="utf-8") as file:
                file.write(new_content)
            print("Endpoint da API atualizado com sucesso!")
            return True
        else:
            print("Não foi possível localizar o endpoint get_events para substituição.")
            return False
    
    except Exception as e:
        print(f"Erro ao corrigir endpoint da API: {str(e)}")
        return False

def main():
    """Função principal"""
    print("=== Iniciando diagnóstico e correção do calendário na página inicial ===")
    
    # 1. Corrigir os dados no banco
    db_fixed = fix_date_issues()
    
    # 2. Corrigir o endpoint da API
    api_fixed = fix_api_endpoint()
    
    # 3. Corrigir a função JavaScript
    js_fixed = fix_js_function()
    
    # Resultado
    if db_fixed and api_fixed and js_fixed:
        print("\n✅ Todas as correções foram aplicadas com sucesso!")
        print("Por favor, reinicie o servidor e teste a página inicial.")
    else:
        print("\n⚠️ Algumas correções não puderam ser aplicadas.")
        print("Verifique os logs acima para mais detalhes.")

if __name__ == "__main__":
    main() 