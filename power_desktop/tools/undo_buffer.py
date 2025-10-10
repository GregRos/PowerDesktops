from __future__ import annotations

from collections import deque
from typing import Deque

from power_desktop.model.model_1d import VdHistoryEntry


class UndoBuffer:
    """
    Undo/redo ring buffer for VdHistoryEntry.

    Storage: deque[VdHistoryEntry] with maxlen=1024

    Behavior:
    - push(state):
        Remove all redo states (anything right of current index), append state,
        and set cursor to the newest item.
    - undo() -> Optional[VdHistoryEntry]:
        Move the cursor one step to the left and return that entry.
        Does not modify the deque.
    - redo() -> Optional[VdHistoryEntry]:
        Move the cursor one step to the right and return that entry.
        Does not modify the deque.
    """

    def __init__(self, initial_state: VdHistoryEntry, maxlen: int = 1024):
        self._buffer: Deque[VdHistoryEntry] = deque(maxlen=maxlen)
        self._buffer.append(initial_state)
        # Cursor points to the current position. After a push, it points to the last element.
        self._index = 0

    def __len__(self) -> int:
        return len(self._buffer)

    def undo(self) -> VdHistoryEntry:
        """
        Returns the previous history entry and moves the cursor left.
        Does not mutate the buffer contents.
        """

        if self._index == 0:
            # Already at the oldest entry
            raise IndexError("Cannot undo further")
        self._index -= 1
        return self._buffer[self._index]

    def redo(self) -> VdHistoryEntry:

        if self._index >= len(self._buffer) - 1:
            # Already at the newest entry
            raise IndexError("Cannot redo further")
        self._index += 1
        return self._buffer[self._index]

    def push(self, state: VdHistoryEntry) -> None:
        top_entry = self._buffer[self._index]
        if state == top_entry:
            return
        # Remove all redo entries
        while len(self._buffer) - 1 > self._index:
            self._buffer.pop()
        # Append and set cursor to newest
        self._buffer.append(state)
        self._index = len(self._buffer) - 1
