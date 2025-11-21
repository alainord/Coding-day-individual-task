from datetime import datetime
from typing import Dict, Any, List


class Device:
    def __init__(self, id: str, name: str, type: str, state: Any = None):
        self.id = id
        self.name = name
        self.type = type  # 'switch' or 'slider' or 'lock'
        self.state = state

    def to_dict(self):
        return {"id": self.id, "name": self.name, "type": self.type, "state": self.state}


# ================================
# INITIAL DEVICES (los de siempre)
# ================================
DEVICES: Dict[str, Device] = {
    "light1": Device("light1", "Living Room Light", "switch", "OFF"),
    "door1": Device("door1", "Front Door", "lock", "LOCKED"),
    "thermostat": Device("thermostat", "Thermostat", "slider", 22.0),
    "ceiling_fan": Device("ceiling_fan", "Ceiling Fan", "slider", 0),
}


# ================================
# ACTION LOG (igual que antes)
# ================================
action_log: List[Dict[str, Any]] = []


def now_str():
    return datetime.now().strftime("%H:%M:%S")


def log_action(device_id: str, action: str, user: str = "User"):
    entry = {"time": now_str(), "device": device_id, "action": action, "user": user}
    action_log.insert(0, entry)


def set_device_state(device_id: str, new_state: Any, user: str = "User"):
    d = DEVICES.get(device_id)
    if not d:
        return
    d.state = new_state
    log_action(device_id, str(new_state), user)


def set_device_value(device_id: str, value: Any, user: str = "User"):
    # for sliders or numeric states
    set_device_state(device_id, value, user)


def get_recent_actions(device_id: str = None, limit: int = 10):
    if device_id:
        return [a for a in action_log if a["device"] == device_id][:limit]
    return action_log[:limit]


# ================================
# ROOMS
# ================================
# Cada room es: { "name": str, "device_ids": [str, ...] }
ROOMS: List[Dict[str, Any]] = []


def add_room(name: str):
    """Add a new room with a given name."""
    # Evitar duplicados tontos por nombre
    for r in ROOMS:
        if r.get("name") == name:
            return
    ROOMS.append({"name": name, "device_ids": []})


def get_rooms():
    """Return list of all rooms."""
    return ROOMS


def _find_room(room_name: str):
    for r in ROOMS:
        if r.get("name") == room_name:
            return r
    return None


def assign_device_to_room(room_name: str, device_id: str):
    """Añadir un device existente a una room."""
    room = _find_room(room_name)
    if not room:
        return
    device_ids = room.get("device_ids")
    if device_ids is None:
        device_ids = []
        room["device_ids"] = device_ids
    if device_id not in device_ids:
        device_ids.append(device_id)

def remove_device_from_room(room_name: str, device_id: str):
    room = _find_room(room_name)
    if not room:
        return
    if device_id in room["device_ids"]:
        room["device_ids"].remove(device_id)

def get_devices_in_room(room_name: str) -> List[Device]:
    """Lista de devices asociados a esa room."""
    room = _find_room(room_name)
    if not room:
        return []
    ids = room.get("device_ids") or []
    return [DEVICES[did] for did in ids if did in DEVICES]


def create_device(name: str, type: str, room_name: str = None, state: Any = None) -> Device:
    """Crear un nuevo dispositivo y (opcionalmente) meterlo en una room."""

    # Estado por defecto según tipo
    if state is None:
        if type == "switch":
            state = "OFF"
        elif type == "lock":
            state = "LOCKED"
        elif type == "slider":
            state = 0

    # Generar id único a partir del nombre
    base_id = name.lower().replace(" ", "_")
    new_id = base_id
    suffix = 1
    while new_id in DEVICES:
        new_id = f"{base_id}_{suffix}"
        suffix += 1

    dev = Device(new_id, name, type, state)
    DEVICES[new_id] = dev

    log_action(new_id, "created", "User")

    if room_name:
        assign_device_to_room(room_name, new_id)

    return dev
