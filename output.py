import const
import inspect  # To manage output verbosity
# from IPython.display import display
import IPython
import numpy as np
from pylatexenc.latex2text import LatexNodes2Text
#import sympy as sym
import mstr




OUTPUT_MODE = const.OUTPUT_UNICODE


def output(content):
    if OUTPUT_MODE == const.OUTPUT_LATEX_MATH:
        output_math(content)
    elif OUTPUT_MODE == const.OUTPUT_UNICODE:
        text = LatexNodes2Text().latex_to_text(str(content))
        output_unicode(text)

def output_unicode(content):
    print(content)

def check_latex_math_output():
    """

    Bibliography:
    - https://discourse.jupyter.org/t/find-out-if-my-code-runs-inside-a-notebook-or-jupyter-lab/6935/3

    :return:
    """
    try:
        ip = IPython.get_ipython()
        if ip is not None:
            return True
        else:
            return False
    finally:
        return False



def set_verbosity_limit(verbosity_limit):
    const.VERBOSITY = verbosity_limit


def output2(lvl, content: mstr.MStr):
    if lvl <= const.VERBOSITY:
        if check_latex_math_output():
            IPython.display.display(content.latex_math)
        else:
            print(content.unicode)


def output_math(math):
    # print(len(inspect.stack()))
    if len(inspect.stack()) < const.VERBOSITY:
        indent = (len(inspect.stack()) - 24) * 5
        indent_latex = f'\\hspace{{{indent}mm}}'
        output = f'{indent_latex}{math}'
        if check_latex_math_output():
            IPython.display.display(IPython.display.Math(output))
        else:
            print(output)


def output_markdown(markdown):
    global VERBOSITY_LIMIT
    if len(inspect.stack()) < VERBOSITY_LIMIT:
        if check_latex_math_output():
            IPython.display.display(IPython.display.Markdown(markdown))
        else:
            print(markdown)

def output_function_title():
    title_level = min(6, - 2 + len(inspect.stack()) - BASE_STACK_LEVEL)
    title_markdown = '#' * title_level
    # print(title_level)
    caller_name = inspect.stack()[1].function
    output = f'{title_markdown} {caller_name}'
    if check_latex_math_output():
        IPython.display.display(IPython.display.Markdown(output))
    else:
        print(output)

def tex(A):
    A = np.array(A)
    latex = f'\\begin{{bmatrix}}'
    if A.ndim == 1:
        row_latex = np.array2string(A, precision=3, separator=' && ')
        row_latex = row_latex.replace('[', '')
        row_latex = row_latex.replace(']', '')
        latex = f'{latex} {row_latex}'
    elif A.ndim == 2:
        for row_index in range(0, A.shape[0]):
            row = A[row_index]
            row_latex = np.array2string(row, precision=3, separator=' && ')
            row_latex = row_latex.replace('[', '')
            row_latex = row_latex.replace(']', '')
            if row_index < A.shape[0] - 1:
                row_latex = f'{row_latex} \\\\'
            latex = f'{latex} {row_latex}'
    latex = f'{latex} \\end{{bmatrix}}'
    return latex

def numpy_array_to_latex_math(numpy_array):
    latex = f'\\begin{{bmatrix}}'
    if numpy_array.ndim == 1:
        row_latex = np.array2string(numpy_array, precision=3, separator=' && ')
        row_latex = row_latex.replace('[', '')
        row_latex = row_latex.replace(']', '')
        latex = f'{latex} {row_latex}'
    elif numpy_array.ndim == 2:
        for row_index in range(0, numpy_array.shape[0]):
            row = numpy_array[row_index]
            row_latex = np.array2string(row, precision=3, separator=' && ')
            row_latex = row_latex.replace('[', '')
            row_latex = row_latex.replace(']', '')
            if row_index < numpy_array.shape[0] - 1:
                row_latex = f'{row_latex} \\\\'
            latex = f'{latex} {row_latex}'
    latex = f'{latex} \\end{{bmatrix}}'
    return latex

