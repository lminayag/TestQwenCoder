# Billetera Digital - MVP

Aplicación móvil de billetera digital desarrollada con **Python**, **Flet**, **SQLAlchemy** y **SQLite**.

## 📱 Características del MVP

### Funcionalidades Principales
- ✅ **Gestión de Cuentas**: Crear, visualizar y administrar múltiples cuentas (efectivo, banco, ahorro, crédito)
- ✅ **Registro de Movimientos**: Registrar ingresos y gastos con descripción y categoría
- ✅ **Seguimiento de Saldos**: Actualización automática de saldos al registrar movimientos
- ✅ **Diseño Mobile-First**: Interfaz optimizada para dispositivos móviles
- ✅ **Historial de Transacciones**: Visualización cronológica de movimientos por cuenta

### Arquitectura del Proyecto
```
/workspace
├── app/
│   ├── models.py      # Modelos SQLAlchemy (Cuenta, Movimiento)
│   ├── services.py    # Lógica de negocio y operaciones CRUD
│   └── main.py        # Interfaz Flet y navegación
├── data/
│   └── wallet.db      # Base de datos SQLite (auto-generada)
└── README.md
```

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.8+
- pip

### Instalación de Dependencias
```bash
pip install flet sqlalchemy
```

### Ejecutar la Aplicación
```bash
cd /workspace
python -m app.main
```

La aplicación se ejecutará automáticamente en modo desktop o web según el entorno.

## 📊 Estructura de Datos

### Tabla: Cuentas
- `id`: Identificador único
- `nombre`: Nombre de la cuenta (ej: "Efectivo", "Banco X")
- `tipo`: general, ahorro, credito
- `saldo_actual`: Saldo actualizado automáticamente
- `moneda`: USD, EUR, etc.

### Tabla: Movimientos
- `id`: Identificador único
- `cuenta_id`: Relación con la cuenta
- `tipo`: ingreso o gasto
- `monto`: Cantidad monetaria
- `descripcion`: Detalle opcional
- `categoria`: Categoría opcional (ej: Alimentos, Transporte)
- `fecha`: Timestamp automático

## 🎨 Diseño UI/UX

### Pantalla Principal
- Tarjeta con saldo total consolidado
- Lista de todas las cuentas con sus saldos
- Botón flotante para agregar nueva cuenta

### Pantalla de Movimientos
- Encabezado con nombre de cuenta y saldo actual
- Lista cronológica de movimientos (ingresos en verde, gastos en rojo)
- Botón para registrar nuevo movimiento

### Diálogos
- Formulario modal para crear cuentas
- Formulario modal para registrar movimientos
- Validaciones básicas de campos

## 🔮 Próximas Mejoras (Post-MVP)

1. **Autenticación**: Login de usuarios múltiples
2. **Transferencias**: Movimientos entre cuentas
3. **Presupuestos**: Límites de gasto por categoría
4. **Reportes**: Gráficos de gastos mensuales
5. **Exportación**: CSV/PDF de movimientos
6. **Modo Oscuro**: Toggle de tema
7. **Backup**: Exportar/importar base de datos
8. **Notificaciones**: Recordatorios de pagos

## 🛠️ Tecnologías

- **Flet**: Framework UI multiplataforma (Flutter-based)
- **SQLAlchemy**: ORM para gestión de base de datos
- **SQLite**: Base de datos ligera embebida
- **Python 3**: Lenguaje principal

## 📝 Notas de Desarrollo

- La base de datos se crea automáticamente en `data/wallet.db`
- Los saldos se actualizan automáticamente al registrar movimientos
- La interfaz es responsive pero optimizada para móvil
- No requiere configuración adicional para empezar a usar

---

**Autor**: Asistente de Desarrollo  
**Licencia**: MIT
