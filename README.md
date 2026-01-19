# SecureApp
## App de seguridad - Security Utility Application

SecureApp es una aplicación de utilidades de seguridad que proporciona funcionalidades esenciales para el desarrollo seguro de aplicaciones. / SecureApp is a security utility application that provides essential functionalities for secure application development.

## 🔒 Características / Features

### 1. Validación de Contraseñas / Password Validation
- Validación de fortaleza de contraseñas
- Verificación de requisitos de seguridad (mayúsculas, minúsculas, números, caracteres especiales)
- Detección de contraseñas comunes
- Sistema de puntuación de seguridad

### 2. Sanitización de Entradas / Input Sanitization
- Prevención de ataques XSS (Cross-Site Scripting)
- Prevención de inyección SQL
- Sanitización de nombres de archivos
- Validación de correos electrónicos
- Prevención de directory traversal

### 3. Cifrado y Hash / Encryption and Hashing
- Cifrado simétrico usando Fernet (AES)
- Generación de claves de cifrado
- Derivación de claves desde contraseñas (PBKDF2)
- Hashing seguro de contraseñas con bcrypt
- Verificación de contraseñas

### 4. Autenticación / Authentication
- Generación de tokens seguros
- Gestión de sesiones
- Validación de tokens
- Generación de códigos 2FA
- Limpieza de sesiones expiradas

## 📋 Requisitos / Requirements

- Python 3.7 o superior
- cryptography >= 41.0.0
- bcrypt >= 4.0.0

## 🚀 Instalación / Installation

1. Clonar el repositorio / Clone the repository:
```bash
git clone https://github.com/Organizacionseven7/SecureApp.git
cd SecureApp
```

2. Instalar dependencias / Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Uso / Usage

### Ejecutar la aplicación de demostración / Run the demo application:
```bash
python main.py
```

### Usar como biblioteca / Use as a library:

```python
# Validación de contraseñas / Password validation
from secure_app.password_utils import PasswordValidator

validator = PasswordValidator()
result = validator.validate("MyPassword123!")
print(f"Valid: {result['valid']}")
print(f"Strength: {result['strength']}")

# Sanitización de entradas / Input sanitization
from secure_app.sanitizer import InputSanitizer

sanitizer = InputSanitizer()
clean_html = sanitizer.sanitize_html("<script>alert('XSS')</script>")
clean_filename = sanitizer.sanitize_filename("../../etc/passwd")

# Cifrado / Encryption
from secure_app.encryption import EncryptionManager

manager = EncryptionManager()
key = manager.generate_key()
manager.set_key(key)
encrypted = manager.encrypt("Secret message")
decrypted = manager.decrypt(encrypted)

# Autenticación / Authentication
from secure_app.auth import AuthManager

auth = AuthManager()
token = auth.create_session("user123")
is_valid = auth.validate_session("user123", token)
```

## 🧪 Pruebas / Testing

Ejecutar todas las pruebas / Run all tests:
```bash
python tests/test_password_utils.py
python tests/test_sanitizer.py
python tests/test_encryption.py
python tests/test_auth.py
```

## 📁 Estructura del Proyecto / Project Structure

```
SecureApp/
├── secure_app/
│   ├── __init__.py           # Inicialización del paquete
│   ├── password_utils.py     # Utilidades de contraseñas
│   ├── sanitizer.py          # Sanitización de entradas
│   ├── encryption.py         # Cifrado y hash
│   └── auth.py               # Autenticación y sesiones
├── tests/
│   ├── test_password_utils.py
│   ├── test_sanitizer.py
│   ├── test_encryption.py
│   └── test_auth.py
├── main.py                   # Aplicación de demostración
├── requirements.txt          # Dependencias
└── README.md                # Documentación

```

## 🔐 Mejores Prácticas de Seguridad / Security Best Practices

1. **Contraseñas**: Siempre use contraseñas fuertes con al menos 12 caracteres
2. **Cifrado**: Nunca almacene claves de cifrado en el código fuente
3. **Sanitización**: Siempre sanitice las entradas del usuario antes de procesarlas
4. **Tokens**: Use tokens seguros y aleatorios para sesiones
5. **Hash**: Use bcrypt para hashear contraseñas, nunca MD5 o SHA1

## 🤝 Contribuciones / Contributing

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Cree una rama para su feature (`git checkout -b feature/AmazingFeature`)
3. Commit sus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abra un Pull Request

## 📄 Licencia / License

Este proyecto está bajo licencia MIT - vea el archivo LICENSE para más detalles.

## 📞 Soporte / Support

Para reportar problemas o solicitar nuevas características, por favor abra un issue en el repositorio de GitHub.

## ✨ Versión / Version

**v0.1.0** - Versión inicial con funcionalidades básicas de seguridad
