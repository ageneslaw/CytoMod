import time
import subprocess
import os.path as op

__all__ = ['toPDF', 'greek2latex']


def toPDF(df, outFn, titStr, float_format='%1.3g'):
    folder, fn = op.split(outFn)
    df = df.applymap(lambda s: s if not isinstance(s, str) else s.replace('_', '-'))
    #     df = df.rename_axis(lambda s: s.replace('_', '-'), axis=1)
    df = df.rename(columns=lambda s: s.replace('_', '-'))
    texFn = outFn[:-3] + 'tex'
    header = ['\\documentclass[10pt]{article}',
              '\\usepackage{lmodern}',
              '\\usepackage{booktabs}',
              '\\usepackage{longtable}',
              '\\usepackage{geometry}',
              '\\usepackage[english]{babel}',
              '\\usepackage[utf8]{inputenc}',
              '\\usepackage{fancyhdr}',
              '\\geometry{letterpaper, landscape, margin=1in}',
              '\\pagestyle{fancy}',
              '\\fancyhf{}',
              '\\rhead{%s}' % time.ctime(),
              '\\chead{%s}' % titStr,
              '\\rfoot{Page \\thepage}',
              '\\begin{document}']

    footer = ['\\end{document}']
    with open(texFn, 'w') as fh:
        for h in header:
            fh.write(h + '\n')
        fh.write(df.to_latex(float_format=lambda f: float_format % f,
                             longtable=True, index=False, escape=False, encoding='utf-8'))
        for f in footer:
            fh.write(f + '\n')
    cmd = ['latex', '-output-format=pdf', '-output-directory=%s' % folder, texFn]

    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    # si.wShowWindow = subprocess.SW_HIDE # default

    subprocess.call(cmd, startupinfo=si)
    """Run latex twice to get the layout correct"""
    subprocess.call(cmd, startupinfo=si)

def greek2latex(s):
    greek = {chr(0x3b1):'$\\alpha$',
             chr(0x3b2):'$\\beta$',
             chr(0x3b3):'$\\gamma$',
             chr(0x3b4):'$\\delta$'}
    for g in list(greek.keys()):
        s = s.replace(g, greek[g])
    return s