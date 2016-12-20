# Module for conversion to Latex.

from Latex import build_pdf

class LatexFile:
    """Object which represents a Latex file."""

    documentContent = '\\begin{document}\n'

    def __init__(self, fileName, policeSize = 11, language='french'):
        self.file = open(fileName, 'w')
        self.policeSize = policeSize
        self.language = language

    def create_header(self):
        self.file.write('\documentclass[{0}, a4paper]'.format(self.policeSize))
        self.file.write('\n\n\\usepackage[utf8]{inputenc}\n\\usepackage[french]{babel}\n\\usepackage[T1]{fontenc}\n')

    def end_document(self):
        self.documentContent = self.documentContent + '\end{document}'
        self.file.write(self.documentContent)

    def build_pdf(self):
        pdfFile = open(self.file.name.replace('.tex', '.pdf'), 'w')
        pdfFile.write(build_pdf(self.file))

    def make_title(self, title='', author='', date=''):
        if title != '':
            self.file.write('\\title{' + title.replace('\n', '\\') + '}\n')

        if author != '':
            self.file.write('\\author{' + author.replace('\n', '\\') + '}\n')

        if date != '':
            self.file.write('\date{' + date.replace('\n', '\\') + '}\n')

    def add_section(self, sectionName: str, isNumber: bool):
        if isNumber:
            self.documentContent += '\section{' + sectionName.replace('\n', '\\') + '}\n'
        else:
            self.documentContent += '\section*{' + sectionName.replace('\n', '\\') + '}\n'

    def add_subsection(self, sectionName: str, isNumber: bool):
        if isNumber:
            self.documentContent += '\subsection{' + sectionName.replace('\n', '\\') + '}\n'
        else:
            self.documentContent += '\subsection*{' + sectionName.replace('\n', '\\') + '}\n'

    def add_subsubsection(self, sectionName: str, isNumber: bool):
        if isNumber:
            self.documentContent += '\subsubsection{' + sectionName.replace('\n', '\\') + '}\n'
        else:
            self.documentContent += '\subsubsection*{' + sectionName.replace('\n', '\\') + '}\n'

    def add_tabular(self, tabular: LatexTabular):
        self.documentContent += tabular.return_latex_tabular()

    def add_itemize(self, itemize: LatexItemize):
        self.documentContent += itemize.return_latex_itemize()

    def str_to_bold(str):
        return '\\texbf{' + str + '}'

    def str_to_italic(str):
        return '\\texit{' + str +'}'

    def str_to_underlined(str):
        return '\\underline{' + str + '}'

    def set_right_alignement(str):
        return '\\begin{flushright}\n\t' + str + '\n\end{flushright}'

    def set_left_alignement(str):
        return '\\begin{flushleft}\n\t' + str + '\n\end{flushleft}'

    def set_center_alignement(str):
        return '\\begin{center}\n\t' + str + '\n\end{center}'

    def add_paragraph(self, str):
        self.documentContent += str.replace('\n', '\\') + '\n\n'



class LatexTabular:
    """Class which represent Latex Table"""
    columnDefinition = ""
    lines = []

    def __init__(self, columnDefinition = "", lines = []):
        self.columnDefinition = columnDefinition
        self.lines = lines

    def add_lines(self, line, isSeparated):
        self.lines.append(line)
        if isSeparated:
            self.lines.append('\hline')

    def add_column(self, column):
        self.columnDefinition = self.columnDefinition + column
        for line in self.lines:
            if line != '\hline':
                line += ' & '

    def add_hline(self):
        self.lines.append('\hline')

    def return_latex_tabular(self):
        finalContent = '\\begin{tabular}{' + self.columnDefinition + '}\n'
        for line in self.lines:
            finalContent += line + '\n\t'

        finalContent += '\end{tabular}\n'
        return finalContent

class LatexItemize:
    environmentType = ''
    itemType = ''
    items = []

    def __init__(self, environmentType = '', itemType = '', items = ''):
        self.environmentType = environmentType
        self.itemType = itemType
        self.items = items

    def set_environment(self, environmentType):
        self.environmentType = environmentType

    def set_item_type(self, itemType):
        self.itemType = itemType

    def add_item(self, item):
        self.items.append(item)

    def return_latex_itemize(self):
        finalContent = '\\begin{' + self.environmentType + '}\n'
        for item in self.items:
            finalContent += '\item[' + self.itemType + '] ' + item + '\n\t'

        finalContent += '\end{' + self.environmentType + '}\n'
        return finalContent