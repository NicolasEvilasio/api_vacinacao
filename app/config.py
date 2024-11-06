"""
Configurações da aplicação.

Este módulo contém as configurações globais da aplicação.
É responsável por:
- Configurar logging
- Definir constantes globais
- Configurar rate limiting
- Gerenciar variáveis de ambiente

Centraliza todas as configurações que podem ser reutilizadas em
diferentes partes da aplicação.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address) 