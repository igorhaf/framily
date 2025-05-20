from fastapi import APIRouter, Depends, HTTPException, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_task import get_multi
from app.core.twilio_config import get_twilio_settings
from twilio.rest import Client
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
        else:
            resp.message("Olá! Para ver a lista de tarefas, envie 'lista de tarefas'.")
        
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