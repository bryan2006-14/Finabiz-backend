from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ===============================
# USUARIO PERSONALIZADO
# ===============================
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(correo, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100, unique=True)
    foto_perfil = models.CharField(max_length=100, blank=True, null=True)
    created_via_social = models.BooleanField(default=False)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.nombre or self.correo


# ===============================
# MODELOS SECUNDARIOS
# ===============================
class UsuarioSocial(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='social_accounts')
    provider = models.CharField(max_length=50)
    provider_id = models.CharField(max_length=200)
    email = models.EmailField(max_length=150, blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuarios_social'


class ChatFinanzas(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='chats')
    mensaje = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_finanzas'


# ===============================
# CATEGORÍAS PREDEFINIDAS
# ===============================
class Categoria(models.Model):
    categoria = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'categorias'

    def __str__(self):
        return self.categoria

    @staticmethod
    def inicializar_categorias():
        """Crea categorías base si no existen."""
        categorias_base = [
            'Alimentación',
            'Transporte',
            'Vivienda',
            'Educación',
            'Salud',
            'Ocio',
            'Servicios',
            'Ropa',
            'Mascotas',
            'Otros',
        ]
        for nombre in categorias_base:
            Categoria.objects.get_or_create(categoria=nombre)


# ===============================
# GASTOS E INGRESOS
# ===============================
class Gasto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='gastos')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    forma_pago = models.CharField(max_length=100)
    fecha = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    nota = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'gastos'

    def __str__(self):
        return f"{self.monto} - {self.usuario}"


class Ingreso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ingresos')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    forma_pago = models.CharField(max_length=100)
    fecha = models.DateField()
    nota = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'ingresos'

    def __str__(self):
        return f"{self.monto} - {self.usuario}"


# ===============================
# LOGROS Y METAS
# ===============================
class TipoLogro(models.Model):
    TIPO_CHOICES = [
        ('primer_gasto', 'Primer Gasto'),
        ('primer_ingreso', 'Primer Ingreso'),
        ('gasto_mensual', 'Gasto Mensual'),
        ('ahorro_mensual', 'Ahorro Mensual'),
        ('consistencia', 'Consistencia'),
        ('meta_ahorro', 'Meta de Ahorro'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, unique=True)
    descripcion = models.TextField()
    icono = models.CharField(max_length=100, default='trophy')
    color = models.CharField(max_length=50, default='#4f46e5')
    meta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tipos_logros'
        verbose_name = 'Tipo de Logro'
        verbose_name_plural = 'Tipos de Logros'

    def __str__(self):
        return self.nombre


class LogroUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='logros')
    tipo_logro = models.ForeignKey(TipoLogro, on_delete=models.CASCADE)
    progreso_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'logros_usuarios'
        unique_together = ['usuario', 'tipo_logro']

    def __str__(self):
        return f"{self.usuario.nombre} - {self.tipo_logro.nombre}"


class MetaAhorro(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('completada', 'Completada'),
        ('vencida', 'Vencida'),
    ]

    ICONO_CHOICES = [
        ('🏠', 'Casa'),
        ('🚗', 'Auto'),
        ('✈️', 'Viaje'),
        ('🎓', 'Educación'),
        ('💍', 'Boda'),
        ('🎁', 'Regalo'),
        ('💼', 'Negocio'),
        ('🏥', 'Salud'),
        ('🎯', 'Objetivo'),
        ('💰', 'Dinero'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='metas')
    nombre_meta = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    meta_total = models.DecimalField(max_digits=12, decimal_places=2)
    monto_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    icono = models.CharField(max_length=10, choices=ICONO_CHOICES, default='🎯')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_objetivo = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')

    class Meta:
        db_table = 'metas'
        verbose_name = 'Meta de Ahorro'
        verbose_name_plural = 'Metas de Ahorro'

    def __str__(self):
        return f"{self.nombre_meta} - {self.usuario.nombre}"

    @property
    def progreso(self):
        if self.meta_total > 0:
            return (self.monto_actual / self.meta_total) * 100
        return 0

    @property
    def dias_restantes(self):
        from django.utils import timezone
        if self.fecha_objetivo:
            dias = (self.fecha_objetivo - timezone.now().date()).days
            return max(0, dias)
        return None
