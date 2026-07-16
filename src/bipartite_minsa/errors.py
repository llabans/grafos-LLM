"""Errores de dominio explícitos."""


class BipartiteMinsaError(Exception):
    """Base para errores controlados del proyecto."""


class SourceValidationError(BipartiteMinsaError):
    """La fuente no satisface el contrato o la guía autorizada."""


class ReconciliationError(BipartiteMinsaError):
    """La fuente primaria y la representación derivada no concuerdan."""


class GraphValidationError(BipartiteMinsaError):
    """Un grafo o sus particiones son inválidos."""


class EvidenceBlockedError(BipartiteMinsaError):
    """Una transformación no puede continuar por evidencia insuficiente."""
