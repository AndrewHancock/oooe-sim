from dataclasses import dataclass, field

class RegisterFile:
    def __init__(self):
        self.isa_registers = {'R' + str(i + 1): 0 for i in range(0,16)}
        self.isa_float_registers = {'F' + str(i + 1): 0 for i in range(0, 16)}
        self.physical_registers = {'P' + str(i + 1): 0 for i in range(0, 16)}
        self.register_allocation_table: dict[str, str] = dict()
        self.allocated_registers: set[str] = set()


    def add_rat_entry(self, reg_label: str, rs_name: str):
        self.register_allocation_table[reg_label] = rs_name

    def get_register_value(self, label: str) -> int:
        if label[0] == 'R':
            return self.isa_registers[label]
        elif label[0] == 'F':
            return self.isa_float_registers[label]
        else:
            raise ValueError(f'Invalid register label: {label}')




