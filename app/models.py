"""
Modelos de base de datos para la billetera digital.
Define las tablas de Cuentas y Movimientos.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///./data/wallet.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Cuenta(Base):
    """Tabla de cuentas (ej: Efectivo, Banco, Tarjeta)"""
    __tablename__ = "cuentas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50), default="general")  # general, ahorro, credito
    saldo_actual = Column(Float, default=0.0)
    moneda = Column(String(10), default="USD")
    created_at = Column(DateTime, default=datetime.now)

    # Relación con movimientos
    movimientos = relationship("Movimiento", back_populates="cuenta", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cuenta(nombre='{self.nombre}', saldo={self.saldo_actual})>"


class Movimiento(Base):
    """Tabla de movimientos (ingresos y gastos)"""
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    cuenta_id = Column(Integer, ForeignKey("cuentas.id"), nullable=False)
    tipo = Column(String(20), nullable=False)  # ingreso, gasto, transferencia
    monto = Column(Float, nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(50), nullable=True)
    fecha = Column(DateTime, default=datetime.now)

    # Relación inversa
    cuenta = relationship("Cuenta", back_populates="movimientos")

    def __repr__(self):
        return f"<Movimiento(tipo='{self.tipo}', monto={self.monto})>"


# Funciones de utilidad para crear tablas y sesiones
def init_db():
    """Inicializa la base de datos creando las tablas"""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Retorna una sesión de base de datos"""
    return SessionLocal()
