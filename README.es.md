[Español](README.es.md) | [English](README.en.md)

---

# DevDrop

DevDrop es una aplicacion de escritorio segura para intercambiar informacion sensible entre dos personas sin exponer datos a servidores, servicios cloud ni autoridades centralizadas.

Los secretos nunca salen del dispositivo sin cifrar. El intercambio funciona mediante copiado y pegado manual, con capacidad offline.

## Caracteristicas

- **Sin backend**: no hay base de datos ni servidor que retenga metadatos.
- **Cifrado extremo a extremo**: mensajes protegidos con AES-GCM.
- **Intercambio de claves fuerte**: X25519 con derivacion HKDF-SHA256.
- **Huella visual**: ayuda a detectar ataques MITM.
- **Nucleo con pocas dependencias**: seguridad apoyada en `cryptography`.
- **UI moderna**: interfaz con Flet y estado local.

## Instalacion

```bash
./init.sh
```

Esto crea `.venv`, instala dependencias y registra el comando `devdrop` en `~/.local/bin`.

Despues ejecuta:

```bash
devdrop
```

o:

```bash
./run.sh
```

## Flujo Offer/Answer

1. El usuario A crea una sesion y obtiene un `Offer`.
2. A envia el `Offer` al usuario B por un canal externo.
3. B pega el `Offer`, lo procesa y genera un `Answer`.
4. B devuelve el `Answer` a A.
5. A procesa el `Answer` y la sesion queda conectada.

## Verificacion de huella

Ambos clientes muestran una huella. Comparala por un canal externo, por ejemplo llamada de voz, para reducir riesgo de intermediario.

## Intercambio de secretos

Usa las pestanas `Send` y `Receive`. Al enviar, DevDrop genera un texto cifrado Base64. Al recibir, pega ese texto y descifralo localmente.

## Seguridad

DevDrop esta disenado para evitar sockets y endpoints remotos arbitrarios. Las claves son de sesion y se eliminan al cerrar la aplicacion.
