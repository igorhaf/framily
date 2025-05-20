from fastapi import APIRouter, Depends, HTTPException, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_task import get_multi
from app.core.twilio_config import get_twilio_settings
from twilio.rest import Client
from app.crud.crud_shopping import shopping_list, shopping_item
import logging
import traceback

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(deps.get_db)):
    """
    Webhook para receber mensagens do WhatsApp via Twilio
    """
    try:
        logger.info("Recebendo webhook do WhatsApp")
        
        # Obter as configurações do Twilio
        try:
            twilio_settings = get_twilio_settings()
            logger.info("Configurações do Twilio carregadas com sucesso")
            logger.info(f"Account SID: {twilio_settings.TWILIO_ACCOUNT_SID[:5]}...")
        except Exception as e:
            logger.error(f"Erro ao carregar configurações do Twilio: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Erro nas configurações do Twilio: {str(e)}")
        
        # Obter os dados do formulário da requisição
        try:
            form_data = await request.form()
            logger.info(f"Form data recebido: {dict(form_data)}")
            message_body = form_data.get("Body", "").lower()
            from_number = form_data.get("From", "")
            logger.info(f"Mensagem recebida: {message_body} de {from_number}")
        except Exception as e:
            logger.error(f"Erro ao processar dados do formulário: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=400, detail=f"Erro ao processar dados da mensagem: {str(e)}")
        
        # Criar resposta
        resp = MessagingResponse()
        
        # Verificar se a mensagem é "lista de tarefas"
        if message_body == "lista de tarefas":
            try:
                # Buscar tarefas no banco de dados
                tasks = get_multi(db=db, limit=10)
                logger.info(f"Tarefas encontradas: {len(tasks)}")
                
                if not tasks:
                    resp.message("Não há tarefas cadastradas no momento.")
                else:
                    # Formatar a lista de tarefas de forma simplificada
                    message = "📋 Lista de Tarefas:\n"
                    for task in tasks:
                        status = "✅" if task.status == "completed" else "⏳"
                        message += f"{task.title} - {status}\n"
                    
                    resp.message(message)
            except Exception as e:
                logger.error(f"Erro ao buscar tarefas: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                resp.message(f"Erro ao buscar tarefas: {str(e)}")
        
        # Verificar se a mensagem é "listas de compras" 
        elif message_body == "listas de compras":
            try:
                # Buscar listas de compras no banco de dados
                shopping_lists = shopping_list.get_multi(db=db, limit=10)
                logger.info(f"Listas de compras encontradas: {len(shopping_lists)}")
                
                if not shopping_lists:
                    resp.message("Não há listas de compras cadastradas no momento.")
                else:
                    # Formatar as listas de compras
                    message = "🛒 Listas de Compras:\n"
                    for shop_list in shopping_lists:
                        item_count = len(shop_list.items)
                        message += f"• {shop_list.name} ({item_count} itens)\n"
                    
                    message += "\nEnvie o nome de uma lista para ver seus itens."
                    resp.message(message)
            except Exception as e:
                logger.error(f"Erro ao buscar listas de compras: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                resp.message(f"Erro ao buscar listas de compras: {str(e)}")
        
        # Verificar se a mensagem corresponde a alguma lista de compras
        else:
            try:
                # Procurar por uma lista que corresponda à mensagem (case insensitive)
                # Primeiro tentamos encontrar correspondências exatas
                shop_list = None
                shop_lists = shopping_list.get_multi(db=db)
                
                # Procura por correspondência exata (case insensitive)
                for lista in shop_lists:
                    if lista.name.lower() == message_body.lower():
                        shop_list = lista
                        break
                
                # Se não encontrou, procura por correspondência parcial
                if not shop_list:
                    for lista in shop_lists:
                        if message_body.lower() in lista.name.lower():
                            shop_list = lista
                            break
                
                if shop_list:
                    # Mostrar os itens da lista
                    if not shop_list.items:
                        resp.message(f"A lista '{shop_list.name}' está vazia.")
                    else:
                        message = f"🛒 Itens da lista '{shop_list.name}':\n"
                        
                        # Agrupar itens por status
                        pending_items = [item for item in shop_list.items if item.status != "BOUGHT"]
                        bought_items = [item for item in shop_list.items if item.status == "BOUGHT"]
                        
                        # Primeiro mostrar itens pendentes
                        if pending_items:
                            message += "\n📌 Pendentes:\n"
                            for item in pending_items:
                                priority = ""
                                if item.priority == "HIGH":
                                    priority = "⚠️ "
                                elif item.priority == "LOW":
                                    priority = "🔽 "
                                
                                category_icon = "🍎"
                                if item.category == "CLEANING":
                                    category_icon = "🧹"
                                elif item.category == "HYGIENE":
                                    category_icon = "🧼"
                                elif item.category == "HOUSEHOLD":
                                    category_icon = "🏠"
                                
                                message += f"{priority}{category_icon} {item.name} ({item.quantity})\n"
                        
                        # Depois mostrar itens já comprados
                        if bought_items:
                            message += "\n✅ Comprados:\n"
                            for item in bought_items:
                                message += f"{item.name} ({item.quantity})\n"
                        
                        message += "\nTotal: " + str(len(shop_list.items)) + " itens"
                        
                        resp.message(message)
                else:
                    # Mensagem padrão
                    resp.message("Olá! Você pode enviar:\n- 'lista de tarefas' para ver suas tarefas\n- 'listas de compras' para ver suas listas de compras")
            except Exception as e:
                logger.error(f"Erro ao processar listas: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                resp.message(f"Erro ao processar sua mensagem: {str(e)}")
        
        # Retornar a resposta com o cabeçalho correto
        response_content = str(resp)
        logger.info(f"Resposta preparada: {response_content}")
        return Response(content=response_content, media_type="application/xml")
    
    except Exception as e:
        logger.error(f"Erro não tratado no webhook: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        # Em caso de erro, retornar uma resposta com o erro específico
        resp = MessagingResponse()
        resp.message(f"Erro: {str(e)}")
        return Response(content=str(resp), media_type="application/xml")

@router.get("/webhook")
async def whatsapp_webhook_get():
    """
    Endpoint GET para o webhook do Twilio
    """
    logger.info("Recebendo requisição GET no webhook")
    return Response(content="Webhook está funcionando!", media_type="text/plain") 