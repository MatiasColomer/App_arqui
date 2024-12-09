from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS  # Importa el paquete CORS

# Configuración básica de la aplicación Flask
app = Flask(__name__)

# Configuración de la conexión a MySQL (modifica según tus credenciales de XAMPP)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'  # Usuario por defecto de XAMPP
app.config['MYSQL_PASSWORD'] = ''  # Deja vacío si no configuraste una contraseña
app.config['MYSQL_DB'] = 'gastos_comunes'

# Inicialización de MySQL
mysql = MySQL(app)

# Inicializa CORS para permitir solicitudes de cualquier origen (puedes modificarlo según tus necesidades)
CORS(app)

# Rutas de la API
@app.route('/gastos', methods=['POST'])
def generar_gastos():
    """
    Generar gastos comunes.
    Recibe un JSON con el mes y el año.
    """
    data = request.json
    mes = data.get('mes')
    año = data.get('año')
    if not mes or not año:
        return jsonify({'error': 'Faltan datos obligatorios (mes, año)'}), 400

    cursor = mysql.connection.cursor()
    try:
        # Ejemplo: registrar un gasto por cada departamento
        cursor.execute("SELECT id FROM departamentos")  # Ajusta la consulta a tu esquema
        departamentos = cursor.fetchall()
        for dept in departamentos:
            cursor.execute("""
                INSERT INTO gastos_comunes (departamento_id, periodo, monto)
                VALUES (%s, %s, %s)
            """, (dept[0], f"{mes}-{año}", 1000))  # Monto fijo por ejemplo
        mysql.connection.commit()
        return jsonify({'mensaje': 'Gastos generados exitosamente'}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/pago', methods=['POST'])
def registrar_pago():
    """
    Registrar un pago de gasto común.
    """
    data = request.json
    departamento = data.get('departamento')
    periodo = data.get('periodo')
    fecha_pago = data.get('fecha_pago')
    if not departamento or not periodo or not fecha_pago:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    cursor = mysql.connection.cursor()
    try:
        # Verificar si ya existe un pago
        cursor.execute("""
            SELECT id FROM pagos WHERE departamento_id = %s AND periodo = %s
        """, (departamento, periodo))
        if cursor.fetchone():
            return jsonify({'estado': 'Pago duplicado'}), 400

        # Insertar el pago
        cursor.execute("""
            INSERT INTO pagos (departamento_id, periodo, fecha_pago)
            VALUES (%s, %s, %s)
        """, (departamento, periodo, fecha_pago))
        mysql.connection.commit()
        return jsonify({'estado': 'Pago registrado exitosamente'}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/gastos_pendientes', methods=['GET'])
def obtener_gastos_pendientes():
    hasta_mes = request.args.get('hasta_mes')
    hasta_año = request.args.get('hasta_año')

    if not hasta_mes or not hasta_año:
        return jsonify({"error": "Faltan parámetros hasta_mes y hasta_año"}), 400

    try:
        # Asegúrate de que hasta_mes y hasta_año son enteros válidos
        hasta_mes = int(hasta_mes)
        hasta_año = int(hasta_año)

        # Formateamos correctamente la fecha
        hasta_periodo = f"{hasta_año}-{hasta_mes:02d}"  # Esto debería ser 'YYYY-MM'

        cursor = mysql.connection.cursor()
        query = """
            SELECT g.id, d.nombre AS departamento, g.periodo, g.monto
            FROM gastos_comunes g
            JOIN departamentos d ON g.departamento_id = d.id
            WHERE g.periodo <= %s
            AND NOT EXISTS (
                SELECT 1 FROM pagos p
                WHERE p.departamento_id = g.departamento_id
                AND p.periodo = g.periodo
            );
        """
        cursor.execute(query, (hasta_periodo,))
        gastos_pendientes = cursor.fetchall()

        result = []
        for row in gastos_pendientes:
            result.append({
                "id": row[0],
                "departamento": row[1],
                "periodo": row[2],
                "monto": float(row[3]),
                "estado": "pendiente"
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Ejecutar el servidor
if __name__ == '__main__':
    app.run(debug=True)
