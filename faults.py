# FILE: faults.py
# DESCRIPTION:
#   Fault data structures and operations for the Automatic Test Generator (ATG).
#   This file defines:
#       - FaultClass: equivalence/dominance fault class
#       - FaultEngine: holds all fault-related state and algorithms for a Circuit

from __future__ import annotations
from B_logic import g_types, int_inverse, TGM, L
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # These imports are ONLY for type checking, not executed at runtime
    from Circ import Circuit, gate


class fault_tv:  # Fault Test Vector
    TG_method: TGM = None
    fault_line: str
    SSA: L

    pass


class f_tvs:  # Fault Test Vectors

    remain: dict[str, set[int]] = None  # Faults requiring

    def add_fault_tv(self):
        pass


class D_fault_tv(fault_tv):
    pass


class EquivalenceFaultClass:
    """
    Represents a class (group) of related faults, such as:
      - structurally equivalent faults
      - faults in a dominance relationship (with one designated representative)
    """

    def __init__(self):
        self.lines: set[tuple[str, int]] = set()
        self.selected_f: tuple[str, int] | None = None

    def add_line(self, line_id: str, sa_val: int) -> None:
        self.lines.add((line_id, sa_val))


class DominanceFaultClass:
    """
    Represents a class (group) of related faults, such as:
      - structurally equivalent faults
      - faults in a dominance relationship (with one designated representative)
    """

    def __init__(self):
        self.lines: set[tuple[str, int]] = set()
        self.selected_f: tuple[str, int] | None = None
        self.union: list[EquivalenceFaultClass] = []

    def add_line(self, line_id: str, sa_val: int) -> None:
        self.lines.add((line_id, sa_val))


class FaultState:
    """Container for all fault-related state for a Circuit."""
    universe: dict[str, set[int]] = {}
    universe_coll: dict[str, set[int]] = {}
    Dclasses: list[DominanceFaultClass] = []
    Eclasses: list[EquivalenceFaultClass] = []


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
        self.state.universe.clear()
        self.state.universe = {}
        u = self.state.universe

        self.state.universe_coll.clear()
        self.state.universe_coll = {}
        cu = self.state.universe_coll

        circ = self.circ

        # Primary inputs
        for inp in circ.Primary_in:
            u[inp] = {0, 1}
            cu[inp] = {0, 1}

        # Fanouts
        for fanout in circ.fanouts:
            fanout_line = circ.get_line(fanout)
            if fanout not in u:
                u[fanout] = {0, 1}
                cu[fanout] = {0, 1}

            for nxt_line in fanout_line.nxt:
                u[nxt_line] = {0, 1}
                cu[nxt_line] = {0, 1}

    def collapse(self) -> None:
        """
        Fault collapsing logic (refactored from Circuit.fault_collapse).
        """
        circ = self.circ
        rel_gates: set[str] = set()
        rel_lines: set[str] = set()

        # Traverse from primary inputs one level forward as before with related lines and gates
        for inp in circ.Primary_in:

            if circ.get_line(inp).is_fanout:
                for l in circ.get_line(inp).nxt:
                    g = circ.get_gate(l)
                    rel_lines.add(l)
                    if g.gate_line_output not in rel_lines:
                        rel_lines.add(g.gate_line_output)
                    if g.gate_id not in rel_gates:
                        rel_gates.add(g.gate_id)
                continue

            g = circ.get_gate(inp)
            if not g:
                continue
            rel_lines.add(inp)

            if g:
                if g.gate_line_output not in rel_lines:
                    rel_lines.add(g.gate_line_output)
                if g.gate_id not in rel_gates:
                    rel_gates.add(g.gate_id)

        # Create Equivalence and Dominance Faults
        self._fault_check(rel_gates)

        # Store collapsed faults

        collapsed_f: list[tuple[str, int]] = []
        for fc in self.state.Eclasses:
            for f in fc.lines:
                if not f == fc.selected_f:
                    if f[0] in circ.Primary_in:
                        collapsed_f.append(f)

        for fc in self.state.Dclasses:
            collapsed_f.append(fc.selected_f)
            if fc.union:
                for u in fc.union:
                    collapsed_f.append(u.selected_f)

        # Collapsing Occurs Below Here

        for l, f in self.state.universe.items():
            for coll_l, sa in collapsed_f:
                if l == coll_l:
                    self.state.universe_coll[l].remove(sa)

    def print_universe(self) -> None:
        """
        Pretty-print the current fault universe and classes.
        """
        import colorama as cl  # local import to avoid forcing colorama on non-CLI code
        cl.init(autoreset=True)

        cu = self.state.universe
        Dclasses = self.state.Dclasses
        Eclasses = self.state.Eclasses

        total_faults_est = len(cu) * 2

        # Print Fault Universe

        print(
            f'    {cl.Back.RED} FAULT UNIVERSE {cl.Back.RESET}'
            f'{cl.Fore.RED} (total: {total_faults_est})'
        )

        for line_id, sa_set in cu.items():
            print(f' {cl.Fore.RED}  {line_id}', end="")
            for fault in sa_set:
                print(f' SA{str(fault)} ', end="")

            print('\n', end="")

        # PRINT FAULT CLASSES BOTH EQUIVALENT AND DOMINANCE

        print(
            f'\n    {cl.Back.RED} FAULT CLASSES {cl.Back.RESET}'
            f'{cl.Fore.RED} (total: {len(Dclasses) + len(Eclasses)})'
        )

        # PRINT FAULT CLASSES BOTH EQUIVALENT AND DOMINANCE
        # PRINT DOMINANCE

        for fc in Dclasses:
            print(f' {cl.Fore.RED}  DOMINANCE  ')
            for l, sa in fc.lines:
                print(f' {l, sa} ', end="")
                if fc.selected_f[0] == l:
                    print(f'   {cl.Back.WHITE} DOMINATES ', end="")
                print('\n', end="")
            if fc.union:
                print(f'      UNION')
                for u in fc.union:
                    print(f'        {u.selected_f}')
            print('\n', end="")

        # PRINT EQUIVALENCE
        for fc in Eclasses:
            print(f' {cl.Fore.RED}  EQUIVALENCE  ')
            for l, sa in fc.lines:
                print(f' {l, sa} ', end="")
                if fc.selected_f[0] == l:
                    print(f'   {cl.Back.WHITE} SELECTED ', end="")
                print('\n', end="")
            print('\n', end="")

        # PRINT COLLAPSED FAULT UNIVERSE

        print(
            f'    {cl.Back.MAGENTA} FAULT COLLAPSED UNIVERSE {cl.Back.RESET}  {cl.Fore.MAGENTA} total: {sum(len(s) for s in self.state.universe_coll.values())}'
        )

        for line_id, sa_set in self.state.universe_coll.items():
            print(f' {cl.Fore.MAGENTA}  {line_id}', end="")
            for SSAval in sa_set:
                print(f' SA{str(SSAval)} ', end="")

            print('\n', end="")

        print('==========FINISHED=========')

    def _fault_check(self, gate_list: set) -> None:
        """
        Internal helper implementing your old Circuit.fault_check logic.
        """
        for rg in gate_list:
            g = self.circ.get_gate(rg)

            if g.type is g_types.XOR:
                return

            # Controlling value and inverse value for fault reduction
            C = g.type.value[0]
            i = g.type.value[1]

            # Dominance Classes
            self._fault_dom_check(g, C, i)

        for rg in gate_list:
            g = self.circ.get_gate(rg)

            if g.type is g_types.XOR:
                return

            # Controlling value and inverse value for fault reduction
            C = g.type.value[0]
            i = g.type.value[1]

            # Equivalence Classes
            self._fault_equ_check(g, C, i)

    def _fault_dom_check(self, g: gate, C: int, i: int):
        # Dominance Classes
        fc = DominanceFaultClass()
        if i:
            fc.selected_f = (g.gate_line_output, C)
            fc.add_line(g.gate_line_output, C)
        else:
            fc.add_line(g.gate_line_output, int_inverse(C))
            fc.selected_f = (g.gate_line_output, int_inverse(C))
        for g_inp in g.gate_line_inputs:
            f = (g_inp, int_inverse(C))
            fc.add_line(*f)
        self.state.Dclasses.append(fc)
        pass

    def _fault_equ_check(self, g: gate, C: int, i: int):
        # Equivalence Classes
        fc = EquivalenceFaultClass()
        if i:
            fc.add_line(g.gate_line_output, int_inverse(C))
        else:
            fc.add_line(g.gate_line_output, C)
        for g_inp in g.gate_line_inputs:

            # Check for Dominance Classes that Dominate Equivalence Class
            for D_fc in self.state.Dclasses:
                if g_inp == D_fc.selected_f[0]:
                    D_fc.union.append(fc)

            f = (g_inp, C)  # (Line, SSA val)
            fc.add_line(*f)

            if not fc.selected_f:
                if g_inp in self.circ.Primary_in:
                    fc.selected_f = f
                if self.circ.get_line(g_inp).is_split:
                    fc.selected_f = f

        if not fc.selected_f:
            fc.selected_f = ('ERROR NO SELECTED LINE IN EQUIVALENT CLASS', 999)

        self.state.Eclasses.append(fc)
        pass
