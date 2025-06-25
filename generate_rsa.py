import ipaddress
from datetime import datetime, timedelta, timezone

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

# === Generate private key ===
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# ===  Create certificate subject and issuer ===
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MyOrg"),
    x509.NameAttribute(NameOID.COMMON_NAME, "chat.local"),
])

# === Build certificate ===
cert = (x509.CertificateBuilder().subject_name(subject).issuer_name(
    issuer).public_key(private_key.public_key()).serial_number(
        x509.random_serial_number()).not_valid_before(
            datetime.now(timezone.utc)).not_valid_after(
                datetime.now(timezone.utc) +
                timedelta(days=365)).add_extension(
                    x509.SubjectAlternativeName([
                        x509.DNSName("chat.local"),
                        x509.DNSName("localhost"),
                        x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                    ]),
                    critical=False,
                ).sign(private_key, hashes.SHA256()))

# === Write private key to PEM ===
with open("key.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,  # PKCS#1
            encryption_algorithm=serialization.NoEncryption(),
        ))

# === Write certificate to PEM ===
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("key.pem and cert.pem generated successfully!")
