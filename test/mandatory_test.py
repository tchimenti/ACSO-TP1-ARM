import pytest
from test_utils import build_testdata

testdata, ids = build_testdata('mandatory')

@pytest.mark.parametrize("ref_states, user_states", testdata, ids=ids)
def test_dumpsim(ref_states, user_states):
    assert len(ref_states) == len(user_states), (
        f"Cantidad de estados distinta: ref={len(ref_states)}, user={len(user_states)}"
    )

    for i, (ref, user) in enumerate(zip(ref_states, user_states)):
        ctx = f"[estado {i} | instruccion {ref.get('instruction_count')}]"

        assert ref["instruction_count"] == user["instruction_count"], (
            f"{ctx} instruction_count: ref={ref['instruction_count']}, user={user['instruction_count']}"
        )
        assert ref["pc"] == user["pc"], (
            f"{ctx} PC: ref={hex(ref['pc'])}, user={hex(user['pc'])}"
        )
        assert ref["flag_n"] == user["flag_n"], (
            f"{ctx} FLAG_N: ref={ref['flag_n']}, user={user['flag_n']}"
        )
        assert ref["flag_z"] == user["flag_z"], (
            f"{ctx} FLAG_Z: ref={ref['flag_z']}, user={user['flag_z']}"
        )

        for reg, ref_val in ref["registers"].items():
            user_val = user["registers"].get(reg)
            assert ref_val == user_val, (
                f"{ctx} registro {reg}: ref={hex(ref_val)}, user={hex(user_val) if user_val is not None else None}"
            )

        for addr, ref_val in ref["memory"].items():
            user_val = user["memory"].get(addr)
            assert ref_val == user_val, (
                f"{ctx} memoria {hex(addr)}: ref={hex(ref_val)}, user={hex(user_val) if user_val is not None else None}"
            )
