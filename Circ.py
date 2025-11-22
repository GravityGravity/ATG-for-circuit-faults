# FILE: Circ.py
# DESCRIPTION:
#   Core circuit data structures used by the Automatic Test Generator (ATG).
#   This file defines:
#       - Circuit: container for gates, lines, fanouts, and fault information
#       - line:    single signal line/net in the circuit
#       - gate:    logic gate with input and output line IDs
#       - fault_class: grouping of equivalent / dominating faults
#
#   The Circuit class is intended to be filled by a parser (e.g., ANTLR listener)
#   and then used by fault generation, fault collapsing, and ATPG algorithms
#   such as the D-algorithm or PODEM.

from enum import Enum, auto
from B_logic import *
import colorama as cl
from faults import FaultEngine

cl.init(autoreset=True)


class gate:
    """
    Represents a logic gate in the circuit.

    Attributes:
        gate_id:           Unique gate identifier.
        type:              Gate type (from g_types enum).
        gate_line_inputs:  List of input line IDs.
        gate_line_output:  Output line ID.
    """

    def __init__(self, gid: str, gtype: g_types, g_inputs: list[str], g_output: str):
        """
        Initialize a gate.

        Args:
            gid:      Gate identifier.
            gtype:    Gate type (from g_types).
            g_inputs: List of input line IDs.
            g_output: Output line ID.
        """
        self.gate_id = gid
        self.type = gtype
        self.gate_line_inputs = g_inputs
        self.gate_line_output = g_output

    def g_change_input(self, old_line_id: str, new_line_id: str):
        """
        Replace one of the gate's input line IDs with a new one.

        Used during fanout splitting to rewire gate inputs from stem to branch.

        Args:
            old_line_id: Existing input line ID to be replaced.
            new_line_id: New input line ID to substitute.
        """
        indx = self.gate_line_inputs.index(old_line_id)
        self.gate_line_inputs[indx] = new_line_id


class line:
    """
    Represents a single signal line (net) in the circuit.

    Attributes:
        line_id:   Line identifier (string).
        values:    Placeholder for logic values over time (if needed).
        nxt:       Set of IDs that this line drives (gate IDs or branch line IDs).
        is_fanout: True if this line is a fanout stem (drives > 1 destination).
    """

    def __init__(self, lid: str):
        """
        Initialize a line with the given ID.

        Args:
            lid: Line identifier.
        """
        self.line_id: str = lid
        self.values: list = []
        self.nxt: set[str] = set()
        self.is_fanout: bool = False

    def fan_out_change(self, fan_out: bool):
        """
        Mark this line as a fanout stem or not.

        Args:
            fan_out: True to mark as fanout stem, False otherwise.
        """
        self.is_fanout = fan_out

    def add_nxt(self, item_id: str):
        """
        Add a destination driven by this line.

        Args:
            item_id: ID of the driven object (typically a gate ID or branch line ID).
        """
        self.nxt.add(item_id)


class Circuit:
    """
    Represents a combinational circuit with:
      - primary inputs and outputs
      - internal lines and gates
      - fanout stems
      - fault universe and collapsed fault sets

    The Circuit is the main container that ATG algorithms will operate on.
    """

    def __init__(self, name: str):
        """
        Initialize an empty circuit with the given name.
        """
        self.circuit_name: str = name

        # Primary inputs/outputs are stored as sets of line IDs.
        self.Primary_in: set[str] = set()
        self.Primary_out: set[str] = set()

        # Gate ID -> gate object
        self.gates: dict[str, gate] = {}

        # Line ID -> line object
        self.lines: dict[str, line] = {}
        # Set of line IDs that are fanout stems (i.e., drive multiple destinations).
        self.fanouts: set[str] = set()
        self.faults: FaultEngine = None

    # -------------------------------------------------------------------------
    # Circuit construction
    # -------------------------------------------------------------------------

    def add_gate(self, gid: str, gtype: g_types, g_inputs: list[str], g_output: str):
        """
        Add a gate to the circuit, creating any missing input/output lines.

        Behavior:
          - Ensures each input line exists; if it doesn't, a new line is created.
          - Registers the gate as a 'next' element of each input line.
          - Detects fanout stems: if a line drives > 1 gate, it becomes a fanout.
          - Ensures the output line exists; if it doesn't, a new line is created.
          - Creates and stores the gate object.

        Args:
            gid:      Unique gate identifier.
            gtype:    Gate type (from g_types enum in B_logic).
            g_inputs: List of input line IDs.
            g_output: Output line ID.
        """
        for inp in g_inputs:
            # Ensure the input line object exists; if not, create it.
            inp_line = self.lines.get(inp)
            if not inp_line:
                msg = (
                    f'ERROR(Circ.py): add_gate() input line does not exist \\{inp}. '
                    f'Creating new line...'
                )
                print(cl.Fore.RED + '    ' + msg)
                inp_line = self.add_line(inp)

            # Register this gate as the destination of the input line.
            inp_line.nxt.add(gid)

            # If more than one gate is connected from this line, mark it as a fanout branch.
            if len(inp_line.nxt) > 1:
                if not inp_line.is_fanout:
                    inp_line.fan_out_change(True)
                if inp_line.line_id not in self.fanouts:
                    self.fanouts.add(inp_line.line_id)

        # Ensure the output line exists.
        if not self.lines.get(g_output):
            temp_line = line(g_output)
            self.lines[g_output] = temp_line

        # Create and register the gate object.
        g = gate(gid, gtype, g_inputs, g_output)
        print(
            f'     {cl.Fore.GREEN}__Created New Gate {cl.Fore.WHITE}{g.gate_id} ')
        self.gates[gid] = g

    def add_line(self, lid: str) -> "line":
        """
        Add a new line to the circuit.

        Behavior:
          - Raises an error if the line already exists.
          - Creates a new line object and registers it in self.lines.

        Args:
            lid: New line identifier.

        Returns:
            The newly created line object.
        """
        # Ensure we do not accidentally overwrite an existing line.
        if self.lines.get(lid):
            msg = (
                f'ERROR(Circ.py): add_line() line already exists \\{lid} in dict. '
                f'EXITING...'
            )
            print(cl.Fore.RED + '    ' + msg)
            raise KeyError(msg)

        l = line(lid)
        print(
            f'     {cl.Fore.BLUE}_Created New Line {cl.Fore.WHITE}{l.line_id} ')
        self.lines[lid] = l

        return self.lines[lid]

    def get_line(self, s_lid: str):
        """
        Retrieve a line object by its ID.

        Args:
            s_lid: Line identifier.

        Returns:
            line object if it exists; otherwise None.
        """
        return self.lines.get(s_lid)

    def get_gate(self, id: str) -> "gate | None":
        """
        Retrieve a gate object.

        Args:
            id: Either a gate ID or a line ID.

        Returns:
            gate object if found; otherwise None.

        Raises:
            KeyError: If attempting to resolve a fanout stem line to a single gate.
        """
        # First treat 'id' as a line ID.
        line_obj: line = self.get_line(id)
        if line_obj:
            # If this is a fanout stem, there is no single gate associated with it.
            if line_obj.is_fanout:
                msg = (
                    f'ERROR(Circ.py): get_gate() cannot get gate from fanout line '
                    f'\\{id}. EXITING...'
                )
                print(cl.Fore.RED + '    ' + msg)
                raise KeyError(msg)

                # Otherwise, the line should drive exactly one gate; pick that gate ID.

            if not line_obj.nxt:
                # Optional: fall back to "producer" search, or just return None.
                return None

            return self.gates.get(next(iter(line_obj.nxt)))

        # Not a line ID; treat it as a gate ID.
        return self.gates.get(id)

    def fanout_split(self):
        """
        Split each fanout stem line into distinct branch lines.

        For each fanout stem F:
          - For each gate G in F.nxt, create a new line "F.i" and connect it to G.
          - Replace F.nxt with the set of newly created branch line IDs.
          - Update each gate's input list so it now uses the split line instead of F.

        This is useful in some ATPG / DFT flows where explicit fanout branches
        are modeled as separate lines.
        """
        for fanout in self.fanouts:
            print(fanout)
            fanout_line = self.lines.get(fanout)
            src_line_nxt = set()

            # For each destination gate, create a split line and rewire.
            for i, nxt_gate in enumerate(fanout_line.nxt):
                print(i)

                # Create new split line (e.g., "g.1", "g.2", ...).
                split_line_id = fanout + f'.{i + 1}'
                newline = self.add_line(split_line_id)
                newline.add_nxt(nxt_gate)

                # Track the new branch line as the fanout's logical children.
                src_line_nxt.add(split_line_id)

                # Update the gate input to use the new branch line instead of the stem.
                self.get_gate(nxt_gate).g_change_input(fanout, split_line_id)

            # Replace fanout_line.nxt with the set of new branch line IDs.
            fanout_line.nxt = src_line_nxt

    # -------------------------------------------------------------------------
    # Fault Handling
    # -------------------------------------------------------------------------

    def create_fault_universe(self) -> None:
        self.faults = FaultEngine(self)
        self.faults.create_universe()

    def fault_collapse(self) -> None:
        self.faults.collapse()

    def print_fault_U(self) -> None:
        self.faults.print_universe()

    # -------------------------------------------------------------------------
    # Circuit printing / debugging
    # -------------------------------------------------------------------------

    def print_circ(self):
        """
        Pretty-print the entire circuit: PIs, POs, lines, fanouts, and gates.

        Intended for debugging and sanity-checking the parsed/constructed circuit.
        """
        print(f'========================================')
        print(f'        {self.circuit_name.upper()}         \n')

        # Primary inputs
        print(f'    {cl.Back.YELLOW} PRIMARY INPUTS ')
        for PI in self.Primary_in:
            print(f' {PI} ', end="")
        print('\n')

        # Primary outputs
        print(f'    {cl.Back.YELLOW} PRIMARY OUTPUTS ')
        for PO in self.Primary_out:
            print(f' {PO} ', end="")
        print('\n', end="")
        print('\n', end="")

        # Lines
        print(
            f'    {cl.Back.BLUE} LINES {cl.Back.RESET}'
            f'{cl.Fore.BLUE} (total: {len(self.lines)})'
        )
        for key, value in self.lines.items():
            print(f' {cl.Fore.CYAN}{key} ->', end="")
            for connected in value.nxt:
                print(f'  {connected} ', end="")

            # Annotate line roles (fanout, PI, PO) for clarity.
            if value.line_id in self.fanouts:
                print(f'   {cl.Fore.BLACK}{cl.Back.WHITE} FANOUT ', end="")
            if value.line_id in self.Primary_in:
                print(f'   {cl.Fore.BLUE}{cl.Back.WHITE} P INPUT ', end="")
            if value.line_id in self.Primary_out:
                print(f'   {cl.Fore.YELLOW}{cl.Back.WHITE} P OUTPUT ', end="")
            print('\n', end="")
        print('\n', end="")

        # Gates
        print(
            f'    {cl.Back.GREEN} GATES {cl.Back.RESET}'
            f'{cl.Fore.GREEN} (total: {len(self.gates)})'
        )
        for key, value in self.gates.items():
            print(f' {key}({value.type.name})')

            print(f' {cl.Fore.GREEN}G_Input: ', end="")
            for Inp in value.gate_line_inputs:
                print(f' {Inp} ', end="")

            print(f' {cl.Fore.MAGENTA}G_Output: ', end="")
            print(f' {value.gate_line_output} ', end="")
            print('\n')

        print('==========FINISHED=========')
