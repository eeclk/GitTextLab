import ast
import streamlit as st
import astor


def extract_modules_from_code(code):
    """Koddan kullanılan modülleri çıkarır"""
    modules = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    modules.append(node.module.split(".")[0])
    except:
        pass
    return modules


def extract_functions_code(code):
    functions = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                name = node.name
                args = [arg.arg for arg in node.args.args]
                docstring = ast.get_docstring(node)
                func_code = astor.to_source(node)

                # Fonksiyon karmaşıklığını hesapla (basit metrik)
                complexity = len(func_code.split("\n"))

                functions.append(
                    {
                        "name": name,
                        "args": args,
                        "docstring": docstring,
                        "lineno": node.lineno,
                        "length": getattr(node, "end_lineno", None) - node.lineno
                        if hasattr(node, "end_lineno")
                        else None,
                        "code": func_code,
                        "complexity": complexity,
                    }
                )
    except SyntaxError as e:
        st.error(f"SyntaxError: {e}")
    return functions
