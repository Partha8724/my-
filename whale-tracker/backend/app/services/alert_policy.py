from collections import defaultdict
from datetime import datetime

from app.services.store import admin_settings


class AlertPolicy:
    def __init__(self) -> None:
        self.last_symbol_emit: dict[str, datetime] = {}
        self.last_signature_emit: dict[str, datetime] = {}
        self.pending_confirmation: dict[str, tuple[int, datetime]] = defaultdict(lambda: (0, datetime.min))

    def should_emit(self, symbol: str, signature: str, confidence: int, timestamp: datetime) -> tuple[bool, str]:
        if confidence < admin_settings["confidence_cutoff"]:
            return False, "below confidence cutoff"

        last_symbol = self.last_symbol_emit.get(symbol)
        if last_symbol and (timestamp - last_symbol).total_seconds() < admin_settings["symbol_cooldown_seconds"]:
            return False, "symbol cooldown"

        last_sig = self.last_signature_emit.get(signature)
        if last_sig and (timestamp - last_sig).total_seconds() < admin_settings["duplicate_suppression_seconds"]:
            return False, "duplicate suppression"

        hits, started = self.pending_confirmation[signature]
        if started == datetime.min or (timestamp - started).total_seconds() > admin_settings["confirmation_window_seconds"]:
            hits, started = 0, timestamp
        hits += 1
        self.pending_confirmation[signature] = (hits, started)
        if hits < admin_settings["confirmation_hits"]:
            return False, "awaiting confirmation"

        self.last_symbol_emit[symbol] = timestamp
        self.last_signature_emit[signature] = timestamp
        self.pending_confirmation[signature] = (0, datetime.min)
        return True, "confirmed"


alert_policy = AlertPolicy()
