""" Agent Memory Map: what he saw """

from dataclasses import dataclass

@dataclass
class MemoryEntry:
    resource_type: str
    last_seen_tick: int

class AgentMemory:
    def __init__(self):
        self._map: dict[tuple[int, int], MemoryEntry] = {}

    def remember(self, position: tuple[int, int], resource_type: str, tick: int) -> None:
        self._map[position] = MemoryEntry(resource_type, tick)

    def forget(self, position: tuple[int, int]) -> None:
        self._map.pop(position, None)

    def known_resources(self) -> list[tuple[int, int]]:
        k_resources: list[tuple[int, int]] = []

        for pos, entry in self._map.items():
            if entry.resource_type == "food":
                k_resources.append(pos)

    def closest_known_resource(self, from_position: tuple[int, int], grid) -> tuple[int, int] | None:
        resources = self.known_resources()
        if not resources:
            return None
        return min(resources, key=lambda pos: grid.toric_distance(from_position, pos))

    def update_from_vision(self, visible_cells: dict[tuple[int, int], str], tick: int) -> None:
         for position, content in visible_cells.items():
            if content == "food":
                self.remember(position, "food", tick)
