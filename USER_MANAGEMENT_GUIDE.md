# Guía: Gestión de Usuarios con Supabase Dashboard

Esta guía te muestra cómo manejar usuarios (invitaciones y reset de contraseña) usando solo el Supabase Dashboard, sin necesidad de código adicional.

---

## 1. Invitar Nuevos Usuarios

### Paso 1: Acceder a Supabase Dashboard
1. Ve a https://supabase.com/dashboard
2. Selecciona tu proyecto
3. En el menú lateral, ve a **Authentication** → **Users**

### Paso 2: Invitar Usuario
1. Click en el botón **"Invite user"** (esquina superior derecha)
2. Ingresa el email del nuevo usuario
3. Click **"Send invitation"**

### Paso 3: Usuario Recibe Email
El nuevo usuario recibirá un email con:
- Link de invitación
- Instrucciones para crear su contraseña
- Link expira en 24 horas

### Paso 4: Usuario Completa Registro
1. Usuario hace click en el link del email
2. Es redirigido a una página de Supabase
3. Ingresa su contraseña deseada
4. Confirma la contraseña
5. Ya puede hacer login en tu dashboard

---

## 2. Reset de Contraseña

### Opción A: Usuario Solicita Reset (Recomendado)

**Configurar en Supabase:**
1. Ve a **Authentication** → **Email Templates**
2. Selecciona **"Reset Password"**
3. Personaliza el template (opcional)
4. Asegúrate que el **Redirect URL** apunte a tu app Streamlit

**Usuario solicita reset:**
1. En el login de tu dashboard, agregar link "¿Olvidaste tu contraseña?"
2. Usuario ingresa su email
3. Recibe email con link de reset
4. Click en link → ingresa nueva contraseña

### Opción B: Admin Resetea Contraseña Manualmente

1. Ve a **Authentication** → **Users**
2. Encuentra al usuario en la lista
3. Click en los 3 puntos (...) al lado del usuario
4. Selecciona **"Send password reset email"**
5. Usuario recibe email con link de reset

---

## 3. Configurar Email Templates

### Personalizar Emails (Opcional pero Recomendado)

1. Ve a **Authentication** → **Email Templates**
2. Verás 4 templates:
   - **Confirm signup**: Email de confirmación de registro
   - **Invite user**: Email de invitación
   - **Magic Link**: Login sin contraseña
   - **Reset Password**: Reset de contraseña

3. Para cada template puedes personalizar:
   - **Subject**: Asunto del email
   - **Body**: Contenido HTML del email
   - **Variables disponibles**:
     - `{{ .ConfirmationURL }}`: Link de confirmación
     - `{{ .Token }}`: Token de autenticación
     - `{{ .SiteURL }}`: URL de tu app

### Ejemplo de Template Personalizado (Reset Password):

```html
<h2>Reset de Contraseña - Panini Dashboard</h2>
<p>Hola,</p>
<p>Recibimos una solicitud para resetear tu contraseña del Panini Dashboard.</p>
<p>Haz click en el siguiente link para crear una nueva contraseña:</p>
<p><a href="{{ .ConfirmationURL }}">Resetear Contraseña</a></p>
<p>Este link expira en 1 hora.</p>
<p>Si no solicitaste este cambio, ignora este email.</p>
<p>Saludos,<br>Equipo Panini Dashboard</p>
```

---

## 4. Configurar URL de Redirección

### Importante: Configurar Site URL

1. Ve a **Authentication** → **URL Configuration**
2. Configura:
   - **Site URL**: `https://tu-app.streamlit.app`
   - **Redirect URLs**: Agrega tu URL de Streamlit
     - `https://tu-app.streamlit.app`
     - `https://tu-app.streamlit.app/**` (con wildcard)

Esto asegura que los links de reset funcionen correctamente.

---

## 5. Gestionar Usuarios Existentes

### Ver Lista de Usuarios
1. **Authentication** → **Users**
2. Verás tabla con:
   - Email
   - Estado (confirmado/pendiente)
   - Fecha de creación
   - Último login

### Acciones Disponibles (menú ...)
- **Send password reset email**: Enviar email de reset
- **Delete user**: Eliminar usuario
- **Ban user**: Bloquear usuario temporalmente

### Filtrar Usuarios
- Usa la barra de búsqueda para encontrar usuarios por email
- Filtra por estado: Confirmed / Unconfirmed

---

## 6. Configuración SMTP (Opcional)

Por defecto, Supabase envía emails desde su servidor. Para emails personalizados:

1. Ve a **Project Settings** → **Auth**
2. Scroll hasta **SMTP Settings**
3. Habilita **Enable Custom SMTP**
4. Configura:
   - Host: `smtp.gmail.com` (o tu proveedor)
   - Port: `587`
   - Username: tu email
   - Password: contraseña de aplicación
   - Sender email: email remitente
   - Sender name: nombre que aparecerá

**Nota**: En el plan gratuito de Supabase, hay límite de 3 emails/hora. Con SMTP propio, no hay límite.

---

## 7. Agregar "Forgot Password" al Login (Opcional)

Si quieres agregar un link en tu dashboard para que usuarios puedan solicitar reset:

**Modificar `streamlit_app/utils/auth.py`:**

```python
def send_password_reset(email):
    """Send password reset email"""
    supabase = get_supabase_client()
    try:
        supabase.auth.reset_password_for_email(email)
        return True
    except Exception as e:
        return False
```

**Modificar `streamlit_app/app.py` (en el login form):**

```python
# Después del botón de login
with st.expander("¿Olvidaste tu contraseña?"):
    reset_email = st.text_input("Ingresa tu email", key="reset_email")
    if st.button("Enviar link de reset"):
        if send_password_reset(reset_email):
            st.success("Email enviado! Revisa tu bandeja de entrada.")
        else:
            st.error("Error al enviar email.")
```

---

## Resumen de Flujos

### Flujo de Invitación
```
Admin → Supabase Dashboard → Invite User
→ Usuario recibe email
→ Usuario crea contraseña
→ Usuario hace login en dashboard
```

### Flujo de Reset de Contraseña
```
Usuario → "Olvidé mi contraseña"
→ Ingresa email
→ Recibe email de reset
→ Click en link
→ Ingresa nueva contraseña
→ Hace login con nueva contraseña
```

---

## Ventajas de Este Enfoque

✅ **Sin código adicional**: Todo manejado por Supabase
✅ **Más seguro**: Supabase maneja tokens y expiración
✅ **Mantenimiento cero**: Actualizaciones automáticas
✅ **Emails profesionales**: Templates personalizables
✅ **Auditoría**: Logs de todos los eventos de auth

---

## Próximos Pasos

1. ✅ Invita tu primer usuario de prueba
2. ✅ Personaliza los email templates
3. ✅ Configura la Site URL
4. ⚠️ (Opcional) Agrega link "Forgot Password" al login
5. ⚠️ (Opcional) Configura SMTP personalizado

---

**¿Necesitas ayuda?**
- Documentación oficial: https://supabase.com/docs/guides/auth
- Email templates: https://supabase.com/docs/guides/auth/auth-email-templates
