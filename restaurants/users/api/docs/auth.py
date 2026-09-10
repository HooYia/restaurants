"""
Documentation Swagger des endpoints d'authentification.
"""

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from ..serializers.mobile_serializers import (
    ErrorResponseSerializer,
    LoginSerializer,
    RegisterOtpSerializer,
    OtpSentSerializer,
    TokenResponseSerializer,
    VerifyOtpSerializer,
)


AUTH_TAG = "Authentification"


register_doc = extend_schema(
    tags=[AUTH_TAG],
    summary="Inscription d'un utilisateur",
    description=(
        "Permet à un nouvel utilisateur de commencer son inscription. "
        "Les informations d'inscription sont enregistrées temporairement "
        "et un code OTP est envoyé par email pour vérifier l'adresse email."
    ),
    request=RegisterOtpSerializer,
    responses={
        201: OpenApiResponse(
            description="OTP envoyé par email. Le même email sera utilisé pour vérifier le code.",
            response=OtpSentSerializer,
            examples=[OpenApiExample(
                "Inscription démarrée",
                value={"detail": "OTP envoyé par email.", "email": "client@example.com"},
            )],
        ),
        400: OpenApiResponse(
            description=(
                "Données invalides, adresse email déjà utilisée "
                "ou numéro de téléphone déjà utilisé."
            ),
            response=ErrorResponseSerializer,
        ),
    },
)


verify_otp_doc = extend_schema(
    tags=[AUTH_TAG],
    summary="Vérifier le code OTP",
    description=(
        "Vérifie le code OTP envoyé lors de l'inscription. "
        "Si le code est valide et non expiré, le compte utilisateur "
        "est créé et des tokens JWT sont retournés."
    ),
    request=VerifyOtpSerializer,
    responses={
        201: OpenApiResponse(
            description=(
                "Inscription validée. Les tokens access et refresh "
                "ainsi que les informations utilisateur sont retournés."
            ),
            response=TokenResponseSerializer,
        ),
        400: OpenApiResponse(
            description="Email inconnu, OTP mal formé, invalide ou expiré.",
            response=ErrorResponseSerializer,
        ),
    },
)


login_doc = extend_schema(
    tags=[AUTH_TAG],
    summary="Connexion utilisateur",
    description=(
        "Authentifie un utilisateur avec ses identifiants "
        "et retourne les tokens JWT access et refresh."
    ),
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description=(
                "Connexion réussie. Les tokens JWT et les "
                "informations de l'utilisateur sont retournés."
            ),
            response=TokenResponseSerializer,
        ),
        400: OpenApiResponse(
            description="Email ou mot de passe incorrect.",
            response=ErrorResponseSerializer,
        ),
    },
)


logout_doc = extend_schema(
    tags=[AUTH_TAG],
    summary="Déconnexion utilisateur",
    description=(
        "Déconnecte l'utilisateur authentifié."
    ),
    responses={
        204: OpenApiResponse(
            description="Déconnexion effectuée avec succès."
        ),
        401: OpenApiResponse(
            description="Jeton JWT absent, invalide ou expiré.",
            response=ErrorResponseSerializer,
        ),
    },
)