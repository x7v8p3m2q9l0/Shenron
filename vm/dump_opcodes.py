
import dis, json, sys
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
    for name, code in sorted(opmap.items(), key=lambda x: x[1]):
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
    dump_opcodes()
