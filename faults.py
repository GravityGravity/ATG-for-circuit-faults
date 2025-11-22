# FILE: faults.py
# DESCRIPTION:
#   Fault data structures and operations for the Automatic Test Generator (ATG).
#   This file defines:
#       - FaultClass: equivalence/dominance fault class
#       - FaultEngine: holds all fault-related state and algorithms for a Circuit

from __future__ import annotations
from B_logic import g_types, int_inverse
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # These imports are ONLY for type checking, not executed at runtime
    from Circ import Circuit, gate


class FaultClass:
    """
    Represents a class (group) of related faults, such as:
      - structurally equivalent faults
      - faults in a dominance relationship (with one designated representative)
    """

    def __init__(self, class_label: str):
        self.lines: set[tuple[str, int]] = set()
        self.class_label: str = class_label
        self.selected_f: str | None = None

    def add_line(self, line_id: str, sa_val: int) -> None:
        self.lines.add((line_id, sa_val))


class FaultState:
    """Container for all fault-related state for a Circuit."""
    universe: dict[str, set[int]] = {}
    universe_coll: dict[str, set[int]] = {}
    classes: list[FaultClass] = []
    line_to_class: dict[str, int] = {}


class FaultEngine:
    """
    Encapsulates all fault-related data and operations for a Circuit.

    Access pattern:
        circ.faults.create_universe()
        circ.faults.collapse()
        circ.faults.print_universe()
    """

    def __init__(self, circuit: Circuit):
        self.circ = circuit          # Back-reference to the owning Circuit
        self.state = FaultState()

    def create_universe(self) -> None:
        """
        Build the initial (un-collapsed) single stuck-at fault universe.

        Policy (same as you had in Circuit.create_fault_universe):
          - Every primary input line gets {SA0, SA1}.
          - Every fanout stem line gets {SA0, SA1}.
          - Every fanout branch (line in fanout_line.nxt) gets {SA0, SA1}.
        """
        cu = self.state.universe
        circ = self.circ

        # Primary inputs
        for inp in circ.Primary_in:
            cu[inp] = {0, 1}

        # Fanouts
        for fanout in circ.fanouts:
            fanout_line = circ.get_line(fanout)
            if fanout not in cu:
                cu[fanout] = {0, 1}

            for nxt_line in fanout_line.nxt:
                cu[nxt_line] = {0, 1}

    def collapse(self) -> None:
        """
        Fault collapsing logic (refactored from Circuit.fault_collapse).
        """
        circ = self.circ
        self.state.universe_coll = self.state.universe.copy()
        rel_gates: set[str] = set()
        rel_lines: set[str] = set()

        # Traverse from primary inputs one level forward as before
        for inp in circ.Primary_in:
            rel_lines.add(inp)

            if circ.get_line(inp).is_fanout:
                for l in circ.get_line(inp).nxt:
                    g = circ.get_gate(l)
                    if g.gate_line_output not in rel_lines:
                        rel_lines.add(g.gate_line_output)
                    if g.gate_id not in rel_gates:
                        rel_gates.add(g.gate_id)
                continue

            g = circ.get_gate(inp)
            if g:
                if g.gate_line_output not in rel_lines:
                    rel_lines.add(g.gate_line_output)
                if g.gate_id not in rel_gates:
                    rel_gates.add(g.gate_id)

        print(rel_lines)
        print(rel_gates)

        for rg in rel_gates:
            g = circ.get_gate(rg)
            self._fault_check(g)

    def print_universe(self) -> None:
        """
        Pretty-print the current fault universe and classes.
        """
        import colorama as cl  # local import to avoid forcing colorama on non-CLI code
        cl.init(autoreset=True)

        cu = self.state.universe
        classes = self.state.classes

        total_faults_est = len(cu) * 2
        print(
            f'    {cl.Back.RED} FAULT UNIVERSE {cl.Back.RESET}'
            f'{cl.Fore.RED} (total: {total_faults_est})'
        )

        for line_id, sa_set in cu.items():
            print(f' {cl.Fore.RED}  {line_id}', end="")
            for fault in sa_set:
                print(f' SA{str(fault)} ', end="")

            print('\n', end="")

        print(
            f'\n    {cl.Back.RED} FAULT CLASSES {cl.Back.RESET}'
            f'{cl.Fore.RED} (total: {len(classes)})'
        )
        sorted_fault_classes = sorted(classes, key=lambda n: n.class_label)
        for fc in sorted_fault_classes:
            print(f' {cl.Fore.RED}  {fc.class_label}')
            for l in fc.lines:
                print(f' {l} ', end="")
                if fc.selected_f == l[0]:
                    if fc.class_label == 'dominance':
                        print(f'   {cl.Back.WHITE} DOMINATED ', end="")
                    if fc.class_label == 'equivalence':
                        print(f'   {cl.Back.WHITE} SELECTED ', end="")
                print('\n', end="")
            print('\n', end="")

        print('==========FINISHED=========')

    def _fault_check(self, g: gate) -> None:
        """
        Internal helper implementing your old Circuit.fault_check logic.
        """
        if g.type is g_types.XOR:
            return

        C = g.type.value[0]
        i = g.type.value[1]

        # Equivalence Classes
        fc = FaultClass('equivalence')
        if i:
            fc.add_line(g.gate_line_output, int_inverse(C))
        else:
            fc.add_line(g.gate_line_output, C)
        for g_inp in g.gate_line_inputs:
            if not fc.selected_f:
                if g_inp in self.circ.Primary_in:
                    fc.selected_f = g_inp
            f = (g_inp, C)
            fc.add_line(*f)
        self.state.classes.append(fc)

        # Dominance Classes
        fc = FaultClass('dominance')
        if i:
            fc.selected_f = g.gate_line_output
            fc.add_line(g.gate_line_output, C)
        else:
            fc.add_line(g.gate_line_output, int_inverse(C))
            fc.selected_f = g.gate_line_output
        for g_inp in g.gate_line_inputs:
            f = (g_inp, int_inverse(C))
            fc.add_line(*f)
        self.state.classes.append(fc)
