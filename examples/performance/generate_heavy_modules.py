with open('heavy_module_annotations.py', 'w') as f:
    f.write("from typing import Any, Dict, Iterator, Mapping, Optional, List, TypeVar, Union\n")
    f.write("from configparser import ConfigParser\n")
    for i in range(2000):
        f.write(f"def f{i}(a: Dict[str, List[Optional[str]]], b: Optional[List[int]]) -> Union[str, bytes]: ...\n")
        f.write(f"def g{i}(a: Optional[ConfigParser], b: Mapping[int, int] = {{}}) -> Any: ...\n")
        f.write(f"def h{i}(a: Any, *args: int) -> Optional[Dict[int, Any]]: ...\n")
        f.write(f"_T{i} = TypeVar('T{i}', bound='C{i}')\n")
        f.write(f"""class C{i}(Iterator[str]):
        field1: 'C{i}'
        field2: Mapping[bytes, str]
        def meth{i}(self: _T{i}, b: int) -> Optional[Dict[str, _T{i}]]:
            ...\n""")
        f.write(f"def i{i}(a: C{i}, b: str = None) -> str: ...\n")

with open('heavy_module_no_annotations.py', 'w') as f:
    f.write("from configparser import ConfigParser\n")
    for i in range(200):
        f.write(f"def f{i}(a, b): ...\n")
        f.write(f"def g{i}(a, b = {{}}): ...\n")
        f.write(f"def h{i}(a, *args): ...\n")
        f.write(f"""class C{i}:
        def meth{i}(self, b):
            ...\n""")
        f.write(f"def i{i}(a, b = None): ...\n")
