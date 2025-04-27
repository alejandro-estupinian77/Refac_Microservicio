from typing import Dict, List, Any
from faker import Faker
from flask import Flask, jsonify, request, Response
import logging
import random
import os

# Configuración de la aplicación
app = Flask(__name__)
fake = Faker()
data = []  # Se inicializa correctamente en main()

# Constantes de configuración
MIN_ITEMS = 1
MAX_ITEMS = 10
MAX_ITEM_ID = 100
DEFAULT_ORDER_COUNT = 1000


class OrderService:
    @staticmethod
    def create_order(order_id: int) -> Dict[str, Any]:
        """
        Crea un pedido con datos aleatorios
        """
        num_items = random.randint(MIN_ITEMS, MAX_ITEMS)
        return {
            'id': order_id,
            'cust': fake.name(),
            'items': [random.randint(1, MAX_ITEM_ID) for _ in range(num_items)]
        }

    @staticmethod
    def create_initial_data(count: int = DEFAULT_ORDER_COUNT) -> List[Dict[str, Any]]:
        """
        Genera un conjunto inicial de pedidos
        """
        return [OrderService.create_order(num) for num in range(1, count + 1)]

    @staticmethod
    def find_by_customer_name(orders: List[Dict[str, Any]], name: str) -> List[Dict[str, Any]]:
        """
        Busca pedidos por nombre de cliente
        """
        return [order for order in orders if name in order['cust']]


# Rutas de la API
@app.route('/api/health', methods=['GET'])
def health_check() -> Response:
    """
    Endpoint para verificar el estado del servicio
    """
    return jsonify({'status': 'healthy'}), 200


@app.route('/allOrders', methods=['GET'])
def all_orders() -> Response:
    """
    Devuelve todos los pedidos
    """
    return jsonify(data), 200


@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id: int) -> Response:
    """
    Devuelve un pedido específico por ID
    """
    try:
        return jsonify(data[order_id - 1]), 200
    except IndexError:
        return jsonify({'error': f'Order with ID {order_id} not found'}), 404


@app.route('/custSearch', methods=['POST'])
def cust_search() -> Response:
    """
    Busca pedidos por nombre de cliente
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    name = json_data.get('name', '')
    result = OrderService.find_by_customer_name(data, name)
    return jsonify(result), 200


@app.errorhandler(Exception)
def handle_exception(e) -> Response:
    """
    Manejador global de excepciones
    """
    app.logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Configuración
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    order_count = int(os.environ.get('ORDER_COUNT', DEFAULT_ORDER_COUNT))
    
    # Inicialización de datos
    data = OrderService.create_initial_data(order_count)
    
    # Configuración de logging
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app.logger.setLevel(log_level)
    
    # Inicio del servidor
    app.logger.info(f"Starting Orders service with {len(data)} orders")
    app.run(debug=debug_mode, host=host, port=port)