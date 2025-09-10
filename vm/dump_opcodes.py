
import dis, json, sys
from vm import OP_HANDLERS
# unused opcode dumper since it won't automatically add the code handlers.
def create_desc(name, code):
    desc = f"Opcode {name} (numeric code {code}) in Python {sys.version_info.major}.{sys.version_info.minor}."
    desc_vi = f"Mã lệnh {name} (số {code}) trong Python {sys.version_info.major}.{sys.version_info.minor}."
    return desc, desc_vi
def dump_opcodes(filename=None):
    ver = f"{sys.version_info.major}_{sys.version_info.minor}"
    if filename is None:
        filename = f"opcodes_py{ver}.json"

    opmap = dis.opmap  
    opcodes = {}
    for name, code in sorted(set(sorted(opmap.items(), key=lambda x: x[1])) - {i for i in [100, 83, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 1, 124, 125, 107, 114, 115, 101, 90, 116, 97, 131, 132, 9, 110, 111, 112, 113, 102, 103, 104, 105, 144, 160, 161, 141, 142, 122, 87, 89, 106, 156, 163, 64, 130, 82, 75, 138, 86, 34, 79, 32, 70, 50, 49, 54, 71, 148, 121, 92, 94, 155, 165, 67, 129, 126, 69, 108, 109, 84, 137, 78, 60, 31, 157, 65, 74, 162, 91, 6, 73, 146, 15, 62, 93, 10, 63, 59, 95, 96, 98, 119, 51, 33, 143, 154, 152, 52, 16, 133, 61, 164, 68, 55, 77, 17, 57, 76, 56, 117, 145, 135]}):
        desc, desc_vi = create_desc(name, code)
        
        try:
            HAVE_ARGUMENT = dis.HAVE_ARGUMENT
        except AttributeError:
            HAVE_ARGUMENT = 90
        has_arg = code >= HAVE_ARGUMENT
        se_noarg = None
        se_witharg = None
        try:
            se_noarg = dis.stack_effect(code)
        except Exception:
            se_noarg = None
        try:
            
            se_witharg = dis.stack_effect(code, 0)
        except Exception:
            se_witharg = None

        opcodes[str(code)] = {
            "name": name,
            "description": desc,
            "description_vi": desc_vi,
            "has_arg": bool(has_arg),
            "stack_effect_noarg": se_noarg,
            "stack_effect_with_arg": se_witharg
        }
    data = {
        "opcodes": opcodes,
        "cmp_op": list(dis.cmp_op)
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # print(f"{len(opcodes)} opcodes")
    return filename

if __name__ == '__main__':
    print(OP_HANDLERS.keys())
    dump_opcodes()
