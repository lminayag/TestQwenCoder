"""
Servicios para la gestión de cuentas y movimientos.
Contiene la lógica de negocio para operaciones CRUD.
"""
from app.models import get_session, Cuenta, Movimiento
from datetime import datetime


class CuentaService:
    """Servicio para gestionar cuentas"""

    @staticmethod
    def crear_cuenta(nombre: str, tipo: str = "general", saldo_inicial: float = 0.0, moneda: str = "USD"):
        """Crea una nueva cuenta"""
        db = get_session()
        try:
            cuenta = Cuenta(
                nombre=nombre,
                tipo=tipo,
                saldo_actual=saldo_inicial,
                moneda=moneda
            )
            db.add(cuenta)
            db.commit()
            db.refresh(cuenta)
            return cuenta
        finally:
            db.close()

    @staticmethod
    def obtener_todas_las_cuentas():
        """Obtiene todas las cuentas"""
        db = get_session()
        try:
            return db.query(Cuenta).all()
        finally:
            db.close()

    @staticmethod
    def obtener_cuenta_por_id(cuenta_id: int):
        """Obtiene una cuenta por su ID"""
        db = get_session()
        try:
            return db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
        finally:
            db.close()

    @staticmethod
    def actualizar_saldo(cuenta_id: int, monto: float):
        """Actualiza el saldo de una cuenta"""
        db = get_session()
        try:
            cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
            if cuenta:
                cuenta.saldo_actual += monto
                db.commit()
                db.refresh(cuenta)
            return cuenta
        finally:
            db.close()


class MovimientoService:
    """Servicio para gestionar movimientos"""

    @staticmethod
    def registrar_movimiento(cuenta_id: int, tipo: str, monto: float, 
                            descripcion: str = None, categoria: str = None):
        """Registra un nuevo movimiento y actualiza el saldo de la cuenta"""
        db = get_session()
        try:
            # Crear el movimiento
            movimiento = Movimiento(
                cuenta_id=cuenta_id,
                tipo=tipo,
                monto=monto,
                descripcion=descripcion,
                categoria=categoria,
                fecha=datetime.now()
            )
            db.add(movimiento)

            # Actualizar saldo de la cuenta
            cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
            if cuenta:
                if tipo == "ingreso":
                    cuenta.saldo_actual += monto
                elif tipo == "gasto":
                    cuenta.saldo_actual -= monto
            
            db.commit()
            db.refresh(movimiento)
            return movimiento
        finally:
            db.close()

    @staticmethod
    def obtener_movimientos_por_cuenta(cuenta_id: int, limite: int = 50):
        """Obtiene los últimos movimientos de una cuenta"""
        db = get_session()
        try:
            return db.query(Movimiento).filter(
                Movimiento.cuenta_id == cuenta_id
            ).order_by(Movimiento.fecha.desc()).limit(limite).all()
        finally:
            db.close()

    @staticmethod
    def obtener_todos_los_movimientos(limite: int = 100):
        """Obtiene todos los movimientos recientes"""
        db = get_session()
        try:
            return db.query(Movimiento).order_by(
                Movimiento.fecha.desc()
            ).limit(limite).all()
        finally:
            db.close()
